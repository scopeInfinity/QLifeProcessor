import logging
from typing import List, Union, Optional

from planner import instruction, unit, util, memory

from planner.asm import line_parser

class LabelsManager:
    def __init__(self):
        self.labels = {}
        self.passive_labels = []

    def add_lazy(self, lazy: unit.LazyLabel):
        if lazy.name == util.LABEL_CONSTANT:
            # do nothing
            return
        self.passive_labels.append(lazy)

    def propogate(self):
        for label in self.passive_labels:
            if label.name not in self.labels:
                raise ValueError(f"'{label.name}' couldn't be resolved")
            label.assign(self.labels[label.name])

    def new_label(self, name: str, value: int):
        label = unit.LazyLabel(name, value)
        assert name not in self.labels, f"repeated label found: {name}"
        # this is already resolved label
        assert isinstance(value, int)
        self.labels[name] = label
        return label


class AsmParser:
    def __init__(self) -> None:
        self.reset()

    def reset(self):
        self.address = 0
        self.lm = LabelsManager()
        self.section = "text"
        # self.ins = []  # type: List[instruction.ParsedInstruction]
        self.final_bytes = []  # type: Union[instruction.ParsedInstruction, unit.Data]

    def get_str(self, resolved=False, rom_binary=False):
        '''Get printable instructions.

        Also removes don't care byte(s) at the end coming
        from .bss section (if rom_binary is true).
        '''
        if rom_binary:
            resolved = True  # implict
        if resolved:
            self.lm.propogate()
        assert memory.LABEL_PROGRAM_ORG in self.lm.labels, f"{memory.LABEL_PROGRAM_ORG} label must be defined"

        track_binary_address = None
        _content = []
        if not rom_binary:
            _content.append(f"{memory.LABEL_PROGRAM_ORG} equ {self.lm.labels[memory.LABEL_PROGRAM_ORG].get()}")
        for add, x in self.final_bytes:
            resolved_instruction_with_address = f"{add:03x}:  {x.get_str(resolved=resolved, binary=False)}"
            if not rom_binary:
                _content.append(resolved_instruction_with_address)
            else:
                if track_binary_address is None:
                    track_binary_address = add # first address can be memory.LABEL_PROGRAM_ORG
                assert track_binary_address == add, "gaps found in binary representation"
                out = f"{x.get_str(resolved=resolved, binary=True)}"
                _content.append(out)
                assert len(out) % 8 == 0, f"failed at {resolved_instruction_with_address}"
                track_binary_address += len(out)//8

        content = '\n'.join(_content)
        if rom_binary:
            _program_content = (content
                .replace("\n", "")
                .replace(" ", "")
                .replace("-", " ")
                .rstrip()
                )
            assert len(_program_content) % 8 == 0
            _program_size = len(_program_content) // 8 # bytes
            assert _program_size < 2**8 # as we are using 1 byte for metadata
            _binary_content = f"{_program_size:08b}" + _program_content
            assert len(_binary_content) % 8 == 0
            assert set(_binary_content) <= set(['0', '1']), "only binary context is expected"

            content = '\n'.join([
                "%s %s %s %s" % (
                    _binary_content[32*i:32*i+8],
                    _binary_content[32*i+8:32*i+16],
                    _binary_content[32*i+16:32*i+24],
                    _binary_content[32*i+24:32*i+32])
                    for i in range((len(_binary_content)+24)//32)
                    ])
        return content

    def get_section(self):
        return self.section

    def section_update(self, name):
        assert name in ["text", "data", "bss"]
        if self.get_section() == "bss" and name != "bss":
            raise ValueError(".bss must be the last section")
        self.section = name

    def get_address(self):
        return self.address

    def add_address(self, add):
        self.address += add

    def add_ins(self, ins: instruction.ParsedInstruction):
        # self.ins.append(ins)
        self.final_bytes.append((self.get_address(), ins))
        self.add_address(ins.size())

    def add_data(self, data: unit.Data):
        self.final_bytes.append((self.get_address(), data))
        self.add_address(data.size())

    def parse_text(self, tokens: List[str], line: str):
        if tokens[0].endswith(":"):
            # label
            assert len(tokens) == 1, "label: should exists in isolation in line"
            assert len(tokens[0]) >= 2, "label should be atleast 1 char long"
            label = tokens[0][:-1]
            self.lm.new_label(label, self.get_address())
            return
        ins_name, tokens = line_parser.parse_line(line)
        if ins_name is None:
            # no instruction
            return
        for _, token in tokens:
            self.lm.add_lazy(token)
        for ins in instruction.parse(ins_name, tokens):
            self.add_ins(ins)

    def parse_data(self, tokens: List[str]):
        label = tokens[0]
        self.lm.new_label(label, self.get_address())

        times = 1
        if tokens[1] == "times":
            times = int(tokens[2])
            tokens = [tokens[0]] + tokens[3:]

        assert len(tokens) == 3, "Three tokens expected in .data other than times"
        if tokens[1] == "db":
            sz = 1
        elif tokens[1] == "dw":
            sz = 2
        elif tokens[1] == "dd":
            sz = 4
        else:
            raise ValueError("unsupported data size provided")

        # unsigned integer only for now
        val = int(tokens[2])
        assert val >= 0 and val < (2**(8*sz))

        for _ in range(times):
            for byte in val.to_bytes(sz, 'little'):
                self.add_data(unit.Data(byte))

    def parse_bss(self, tokens: List[str]):
        nothing_happened = True
        if len(tokens) >= 1 and tokens[0].endswith(":"):
            label = tokens[0][:-1]
            self.lm.new_label(label, self.get_address())
            tokens = tokens[1:]
            nothing_happened = False
        if len(tokens) >= 1 and tokens[0] == "resb":
            sz = int(tokens[1])
            for _ in range(sz):
                self.add_data(unit.Data(None))
            nothing_happened = False
        assert not nothing_happened

    def parse_constant(self, tokens: List[str]):
        assert tokens[1].lower() == "equ"
        self.lm.new_label(tokens[0], int(tokens[2], 0))
        if tokens[0] == memory.LABEL_PROGRAM_ORG:
            assert self.get_address() == 0, f"{memory.LABEL_PROGRAM_ORG} must be the first label defined"
            self.add_address(self.lm.labels[memory.LABEL_PROGRAM_ORG].get())
        return

    def parse_line(self, line: str):
        line = line.strip()
        if len(line) == 0:
            # empty line
            return
        if line.startswith("#"):
            # comment
            return
        # case insensitive
        tokens = [x for x in line.split()]

        if tokens[0].lower() == "section":
            assert len(tokens) == 2,f"expects section <what>, line: {line}"
            assert tokens[1].lower() in [".text", ".data", ".bss"]
            self.section_update(tokens[1][1:].lower())
            return

        if len(tokens) == 3 and tokens[1].lower() == "equ":
            # constants
            self.parse_constant(tokens)
            return

        if self.get_section() == "text":
            self.parse_text(tokens, line)
        elif self.get_section() == "data":
            self.parse_data(tokens)
        elif self.get_section() == "bss":
            self.parse_bss(tokens)
        else:
            raise Exception(f"unknown section: {self.get_section()}")

    def parse_lines(self, lines: List[str]):
        line_no = 1
        for line in lines:
            try:
                self.parse_line(line)
            except ValueError as e:
                raise ValueError(f"Parse failed at {line_no}: {e}\n {line}")
            line_no += 1
