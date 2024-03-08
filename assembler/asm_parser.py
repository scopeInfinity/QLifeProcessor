import re
from typing import List, Union

import unit
import util

DATA_SIZE = 1 # bytes

BOILERPLATE_INS_APPEND = '''
    section .bss
    R0: resb 1
    R1: resb 1
    R2: resb 1
    R3: resb 1
    R4: resb 1
    R5: resb 1
    R6: resb 1
    R8: resb 1
'''

class AsmParser:
    @staticmethod
    def get_instance():
        if not hasattr(AsmParser, "_instance"):
            AsmParser._instance = AsmParser()
        return AsmParser._instance

    def __init__(self) -> None:
        self.reset()

    def reset(self):
        self.address = 0
        self.labels = {}
        self.section = "text"
        self.ins = []  # type: List[unit.unit.Instruction]
        self.final_bytes = []  # type: Union[unit.unit.Instruction, unit.Data]

    def append_boilerplate(self):
        assert not hasattr(self, "_append_boilerplay_run_once")
        for line in BOILERPLATE_INS_APPEND.splitlines():
            self.parse_line(line)
        self._append_boilerplay_run_once = True

    def get_section(self):
        return self.section

    def print(self, resolved=False, rom_binary=False):
        '''Prints the instructions.

        Also removes don't care byte(s) at the end coming
        from .bss section (if rom_binary is true).
        '''
        track_binary_address = None
        _content = []
        for add, x in self.final_bytes:
            if not rom_binary:
                _content.append(f"{add:03x}:  {x.get_str(resolved=resolved, binary=False)}")
            else:
                if track_binary_address is None:
                    track_binary_address = add
                assert track_binary_address == add, "gaps found in binary representation"
                out = f"{x.get_str(resolved=resolved, binary=True)}"
                _content.append(out)
                assert len(out) % 8 == 0
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

            content = '\n'.join([_binary_content[8*i:8*(i+1)] for i in range(len(_binary_content)//8)])

        print(content)

    def section_update(self, name):
        assert name in ["text", "data", "bss"]
        if self.get_section() == "bss" and name != "bss":
            raise ValueError(".bss must be the last section")
        self.section = name

    def get_address(self):
        return self.address

    def add_address(self, add):
        self.address += add

    def new_label(self, label, value = None):
        "new label found for current address"
        assert util.is_valid_label(label), f"'{label}' is not valid"
        assert label not in self.labels.keys(), f"repeated label found: {label}"
        self.labels[label] = value if value is not None else self.get_address()
        assert isinstance(self.labels[label], int)

    def get_label_value(self, label):
        return self.labels[label]

    def add_ins(self, ins: unit.Instruction):
        self.ins.append(ins)
        self.final_bytes.append((self.get_address(), ins))
        self.add_address(ins.size())

    def add_data(self, data: unit.Data):
        self.final_bytes.append((self.get_address(), data))
        self.add_address(data.size())

    def parse_text(self, tokens: List[str]):
        if tokens[0].endswith(":"):
            # label
            assert len(tokens) == 1, "label: should exists in isolation in line"
            assert len(tokens[0]) >= 2, "label should be atleast 1 char long"
            label = tokens[0][:-1]
            self.new_label(label)

        elif tokens[0] == "jmp":
            assert len(tokens) == 2, f"found: {tokens}"
            self.add_ins(unit.Instruction("jmp", unit.OperandC(unit.Label(tokens[1]))))
        elif tokens[0] in ["out"]:
            assert len(tokens) == 3, f"found: {tokens}"
            assert util.is_memory_operand(tokens[2]), f"found: {tokens}"
            # token[1] can be memory or constant
            self.add_ins(unit.Instruction(tokens[0], unit.get_operand_cm(tokens[1]), unit.get_operand_cm(tokens[2])))
        elif tokens[0] in ["in"]:
            assert len(tokens) == 3, f"found: {tokens}"
            assert util.is_memory_operand(tokens[1]), f"found: {tokens}"
            # token[2] can be memory or constant
            self.add_ins(unit.Instruction(tokens[0], unit.get_operand_cm(tokens[1]), unit.get_operand_cm(tokens[2])))
        elif tokens[0] in ["mov", "add", "sub", "shl", "shr", "cmp", "and", "or"]:
            assert len(tokens) == 3, f"found: {tokens}"
            assert util.is_memory_operand(tokens[1]), f"found: {tokens}"
            # token[2] can be memory or constant
            self.add_ins(unit.Instruction(tokens[0], unit.get_operand_cm(tokens[1]), unit.get_operand_cm(tokens[2])))
        elif tokens[0] in ["call", "jneq"]:
            assert len(tokens) == 2, f"found: {tokens}"
            self.add_ins(unit.Instruction(tokens[0], unit.OperandC(unit.Label(tokens[1]))))
        elif tokens[0] in ["hlt", "ret"]:
            assert len(tokens) == 1, f"found: {tokens}"
            self.add_ins(unit.Instruction(tokens[0]))
        else:
            raise ValueError(f"don't recognize the unit.instruction: {tokens}")

    def parse_data(self, tokens: List[str]):
        label = tokens[0]
        self.new_label(label)

        times = 1
        if tokens[1] == "times":
            times = int(tokens[2])
            tokens = [tokens[0]] + tokens[3:]

        assert len(tokens) == 3, "Three tokens expected in .data other than times"
        if tokens[1] == "db":
            sz = 1
        elif tokens[1] == "dw":
            sz = 2
        else:
            raise ValueError("invalid data size provided")

        # unsigned integer only for now
        val = int(tokens[2])
        assert val >= 0 and val < (2**(8*sz))

        for _ in range(times):
            for byte in val.to_bytes(sz, 'big'):
                self.add_data(unit.Data(byte))

    def parse_bss(self, tokens: List[str]):
        if len(tokens) == 3:
            assert tokens[0].endswith(":"), f"bss tokens: {tokens}"
            label = tokens[0][:-1]
            self.new_label(label)
            tokens = tokens[1:]

        assert tokens[0] == "resb"
        sz = int(tokens[1])
        for _ in range(sz):
            self.add_data(unit.Data(None))

    def parse_constant(self, tokens: List[str]):
        assert tokens[1] == "equ"
        self.new_label(tokens[0], int(tokens[2], 0))
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
        tokens = [x for x in re.split(" |,", line.lower()) if len(x) > 0]

        if tokens[0] == "section":
            assert len(tokens) == 2, "expects section <what>"
            assert tokens[1].startswith(".")
            self.section_update(tokens[1][1:])
            return

        if len(tokens) == 3 and tokens[1] == "equ":
            # constants
            self.parse_constant(tokens)
            return

        if self.get_section() == "text":
            self.parse_text(tokens)
        elif self.get_section() == "data":
            self.parse_data(tokens)
        elif self.get_section() == "bss":
            self.parse_bss(tokens)
        else:
            raise Exception(f"unknown section: {self.get_section()}")
