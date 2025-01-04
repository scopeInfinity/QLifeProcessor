from enum import Enum
from typing import List, Union, Tuple

from planner import memory, unit, util

'''
# Stage 0
load instruction
from instrucition
    trim vr_source
    trim vrw_source
    trim MBlockSelector_stage1
    trim MBlockSelector_stage2
    trim alu_op
    trim MBlockSelector_stage3
# Stage 1
vr_value = Mblock(vr_source, MBlockSelector_stage1)

# Stage 2
vrw_value = RAM[vrw_source OR vr_value as MBlockSelector_stage2]

# Stage 3
vw_value = ALU(alu_op, vr_value, vrw_value)

'''


class MBlockSelector_stage1(Enum):
    '''
    bits: [is_io][is_const else ram]
    '''
    VR_SOURCE_RAM = 0
    VR_SOURCE_IO = 2
    VR_SOURCE_CONST = 3
    # last one for reverse lookup
    DONT_CARE = 3

    @classmethod
    def wire(cls, sel) -> List:
        assert isinstance(sel, cls)
        return [sel.value%2, sel.value>>1]

    @classmethod
    def from_binary(cls, bin: List[int]):
        assert len(bin) == 2
        val = bin[0]+bin[1]*2
        assert val >= 0 and val < 4
        return cls(val)

class MBlockSelector_stage2(Enum):
    '''
    bits: [read_ram(vrw_source) else read_ram(vr_value)]
    '''
    VRW_SOURCE_CONST = 4
    VRW_SOURCE_RAM = 0
    VR_VALUE_RAM = 1
    # vr_source<<8 | vrw_source
    # Pretty specific operation for passing 16-bit constant or address
    VR_SOURCE_SHL8_VRW_SOURCE_RAM = 2
    VR_SOURCE_SHL8_VRW_SOURCE_CONST = 6
    PC = 7

    # last one for reverse lookup
    DONT_CARE = 0

    @classmethod
    def wire(cls, sel) -> List:
        assert isinstance(sel, cls)
        return [sel.value%2, (sel.value>>1)%2, sel.value>>2]

    @classmethod
    def from_binary(cls, bin: List[int]):
        assert len(bin) == 3
        val = bin[0]+bin[1]*2+bin[2]*4
        return cls(val)

class MBlockSelector_stage3(Enum):
    NO_WRITE            = 0
    VRW_SOURCE_RAM      = 1
    VRW_SOURCE_IO       = 2
    VRW_VALUE_RAM       = 3
    PC_NEXT             = 4
    PC_NEXT_IF_ZERO     = 5
    PC_NEXT_IF_NOT_ZERO = 6
    HLT                 = 7

    @classmethod
    def wire(cls, sel) -> List:
        assert isinstance(sel, cls)
        return [sel.value%2, (sel.value>>1)%2, sel.value>>2]

    @classmethod
    def from_binary(cls, bin: List[int]):
        assert len(bin) == 3
        val = bin[0]+bin[1]*2+bin[2]*4
        assert val >= 0 and val < 8
        return cls(val)


class ALU(Enum):
    ADD = 0
    SUB = 1
    SHL = 2
    SHR = 3
    PASS_R = 4   # vr_value
    PASS_RW = 5  # vrw_value
    AND = 6
    OR = 7
    XOR = 8
    # vr_value<<8 | vrw_value
    # Pretty specific operation for passing 16-bit long operand value
    R_SHL8_RW_OR = 9

    @staticmethod
    def wire(sel) -> List:
        return [sel.value%2, (sel.value>>1)%2, (sel.value>>2)%2, (sel.value>>3)]

    @classmethod
    def from_binary(cls, bits: List[int]):
        value = bits[0]+bits[1]*2+bits[2]*4+bits[3]*8
        return ALU(value)

    @staticmethod
    def execute(op, rw, r):
        assert rw>=0 and rw<(1<<32)
        assert r>=0 and r<(1<<32)
        MASK = ((1<<32)-1)
        if op == ALU.ADD:
            return MASK&(rw+r)
        if op == ALU.SUB:
            # TODO: deal with negative number
            return MASK&(rw-r)
        if op == ALU.SHL:
            return MASK&(rw<<r)
        if op == ALU.SHR:
            return MASK&(rw>>r)
        if op == ALU.PASS_R:
            return MASK&(r)
        if op == ALU.PASS_RW:
            return MASK&(rw)
        if op == ALU.AND:
            return MASK&(rw&r)
        if op == ALU.OR:
            return MASK&(rw|r)
        if op == ALU.XOR:
            return MASK&(rw^r)
        if op == ALU.R_SHL8_RW_OR:
            return MASK&(rw|(r<<8))
        raise Exception(f"unsupported ALU op: {op}")

MAPPING = {
    "alu_op"    : [0, 1, 2, 3],
    "mblock_s1" : [4, 5],
    "mblock_s2" : [6, 7, 8],
    "mblock_s3" : [9, 10, 11],
}

class EncodedInstruction:
    def __init__(self,
                mblock_s1: MBlockSelector_stage1,
                mblock_s2: MBlockSelector_stage2,
                mblock_s3: MBlockSelector_stage3,
                alu_op: ALU) -> None:
        self.mblock_s1 = mblock_s1
        self.mblock_s2 = mblock_s2
        self.mblock_s3 = mblock_s3
        self.alu_op = alu_op

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, EncodedInstruction):
            return False
        return (self.mblock_s1 == __value.mblock_s1 and
                self.mblock_s2 == __value.mblock_s2 and
                self.mblock_s3 == __value.mblock_s3 and
                self.alu_op == __value.alu_op)

    @staticmethod
    def assign_bits(bits: List[int], name: str, values: List[int]):
        indexs = MAPPING[name]
        assert len(indexs) == len(values)
        for i, j in enumerate(indexs):
            assert values[i] in [0,1]
            bits[j] = values[i]

    @staticmethod
    def get_bits(bits: List[int], name: str):
        return [bits[i] for i in MAPPING[name]]

    def encode(self):
        # value_r  = &mblock_resolve(address_r)
        # value_rw = &mblock_resolve(address_rw)
        # value_rw = op(value_r, [value_rw])

        bits = [0]*16

        # Implemented in encode_full(...)
        # bits[16:24] is address_r (address to read only from)
        # bits[24:32] is address_rw (address to read from or write to)

        self.assign_bits(bits, "mblock_s1", MBlockSelector_stage1.wire(self.mblock_s1))
        self.assign_bits(bits, "mblock_s2", MBlockSelector_stage2.wire(self.mblock_s2))
        self.assign_bits(bits, "mblock_s3", MBlockSelector_stage3.wire(self.mblock_s3))
        self.assign_bits(bits, "alu_op", ALU.wire(self.alu_op))
        return sum([bits[i]<<i for i in range(16)])

    @classmethod
    def from_binary(cls, encoded: int):
        encoded_bits = [1 if (encoded&(1<<i))>0 else 0 for i in range(16)]
        mblock_s1 = MBlockSelector_stage1.from_binary(cls.get_bits(encoded_bits, 'mblock_s1'))
        mblock_s2 = MBlockSelector_stage2.from_binary(cls.get_bits(encoded_bits, 'mblock_s2'))
        mblock_s3 = MBlockSelector_stage3.from_binary(cls.get_bits(encoded_bits, 'mblock_s3'))
        alu_op = ALU.from_binary(cls.get_bits(encoded_bits, 'alu_op'))
        return EncodedInstruction(mblock_s1, mblock_s2, mblock_s3, alu_op)

    def __str__(self):
        return str((self.mblock_s1, self.mblock_s2, self.mblock_s3, self.alu_op))

    def plug(self, address_rw: unit.LazyLabel, address_r: unit.LazyLabel):
        return FullyEncodedInstruction(self, address_rw, address_r)


class FullyEncodedInstruction:
    def __init__(self, encoded_instruction: EncodedInstruction, address_rw: unit.LazyLabel, address_r: unit.LazyLabel) -> None:
        self.address_rw = address_rw
        self.address_r = address_r
        self.encoded_instruction = encoded_instruction

    @classmethod
    def from_binary(cls, ins: List[int]):
        return cls(
            EncodedInstruction.from_binary(ins[0]+(ins[1]<<8)),
            unit.LazyLabel(util.LABEL_CONSTANT, ins[2]),
            unit.LazyLabel(util.LABEL_CONSTANT, ins[3]),
        )

    def get_binary(self, ensure_resolved=False) ->  List[unit.Data]:
        encoded = self.encoded_instruction.encode()
        return [
            unit.Data(encoded%256),
            unit.Data(encoded//256),
            unit.Data(self.address_rw.get(ensure_resolved=ensure_resolved)),
            unit.Data(self.address_r.get(ensure_resolved=ensure_resolved))
        ]

    def __str__(self):
        return str((str(self.encoded_instruction), str({"rw": self.address_rw, "r": self.address_r})))

    def size(self):
        return 4  # bytes


class ParserInstruction:
    def __init__(self, name: str, type_rw: unit.Operand, type_r: unit.Operand, encoded_instruction: EncodedInstruction):
        self.name = name
        self.type_rw = type_rw
        self.type_r = type_r
        self.encoded_instruction = encoded_instruction
        self.is_value_16bit = (encoded_instruction.alu_op == ALU.R_SHL8_RW_OR)
        if self.is_value_16bit:
            assert self.type_rw == self.type_r

    def expect_asm_operands(self):
        if self.is_value_16bit:
            expects = [self.type_r]
        else:
            expects = [self.type_rw, self.type_r]
        return expects

    def parse(self, values: List[Tuple[unit.Operand, int]]):
        return ParsedInstruction(self, values)

    def __str__(self) -> str:
        expects = ', '.join([str(x) for x in self.expect_asm_operands()])
        return "%s %s" % (self.name, expects)


class ParsedInstruction:
    def __init__(self, _parser: ParserInstruction, values: List[Tuple[unit.Operand, unit.LazyLabel]]):
        self.parser = _parser
        self.values = values
        self.fully_encoded_instruction = self.get_fully_encoded_instruction(values)

    def get_fully_encoded_instruction(self, values: List[Tuple[unit.Operand, unit.LazyLabel]]):
        if self.parser.expect_asm_operands() != [t[0] for t in values]:
            raise ValueError(f"{self.parser.name} want operand type {self.parser.expect_asm_operands()}, given operand values {values}")
        if self.parser.is_value_16bit:
            assert len(values) == 1
            address_rw = values[0][1].bin_and(0xFF)
            address_r = values[0][1].shr(8)
        else:
            assert len(values) == 2
            address_rw = values[0][1]
            address_r = values[1][1]
        return self.parser.encoded_instruction.plug(address_rw, address_r)

    def get_str(self, resolved=False, binary=False):
        if binary:
            assert resolved
            return ''.join([x.get_str(binary=True) for x in self.fully_encoded_instruction.get_binary(ensure_resolved=True)])

        printable_values = []
        for val_type, val in self.values:
            assert val_type in [unit.Operand.ADDRESS, unit.Operand.DADDRESS, unit.Operand.CONSTANT]
            if val_type == unit.Operand.ADDRESS:
                printable_values.append("[%s]" % (val.get_str(resolved=resolved)))
            elif val_type == unit.Operand.DADDRESS:
                printable_values.append("[[%s]]" % (val.get_str(resolved=resolved)))
            else:
                printable_values.append("%s" % (val.get_str(resolved=resolved)))
        return "%s %s" % (self.parser.name, ', '.join(printable_values))

    def __str__(self):
        return self.get_str(resolved=False, binary=False)

    def size(self):
        return self.fully_encoded_instruction.size()

INSTRUCTIONS = [
    ParserInstruction("IN", unit.Operand.ADDRESS, unit.Operand.CONSTANT,
                      EncodedInstruction(MBlockSelector_stage1.VR_SOURCE_IO,
                                         MBlockSelector_stage2.DONT_CARE,
                                         MBlockSelector_stage3.VRW_SOURCE_RAM,
                                         ALU.PASS_R)),
    ParserInstruction("OUT", unit.Operand.CONSTANT, unit.Operand.ADDRESS,
                      EncodedInstruction(MBlockSelector_stage1.VR_SOURCE_RAM,
                                         MBlockSelector_stage2.DONT_CARE,
                                         MBlockSelector_stage3.VRW_SOURCE_IO,
                                         ALU.PASS_R)),
    # CALL?
    # HLT?
    ParserInstruction("MOV", unit.Operand.ADDRESS, unit.Operand.ADDRESS,
                      EncodedInstruction(MBlockSelector_stage1.VR_SOURCE_RAM,
                                         MBlockSelector_stage2.DONT_CARE,
                                         MBlockSelector_stage3.VRW_SOURCE_RAM,
                                         ALU.PASS_R)),
    ParserInstruction("MOVC", unit.Operand.ADDRESS, unit.Operand.CONSTANT,
                      EncodedInstruction(MBlockSelector_stage1.VR_SOURCE_CONST,
                                         MBlockSelector_stage2.DONT_CARE,
                                         MBlockSelector_stage3.VRW_SOURCE_RAM,
                                         ALU.PASS_R)),
    ParserInstruction("PCPLUS", unit.Operand.ADDRESS, unit.Operand.CONSTANT,
                      EncodedInstruction(MBlockSelector_stage1.VR_SOURCE_CONST,
                                         MBlockSelector_stage2.PC,
                                         MBlockSelector_stage3.VRW_SOURCE_RAM,
                                         ALU.ADD)),
    ParserInstruction("LOAD", unit.Operand.ADDRESS, unit.Operand.DADDRESS,
                      EncodedInstruction(MBlockSelector_stage1.VR_SOURCE_RAM,
                                         MBlockSelector_stage2.VR_VALUE_RAM,
                                         MBlockSelector_stage3.VRW_SOURCE_RAM,
                                         ALU.PASS_RW)),
    ParserInstruction("STORE", unit.Operand.DADDRESS, unit.Operand.ADDRESS,
                      EncodedInstruction(MBlockSelector_stage1.VR_SOURCE_RAM,
                                         MBlockSelector_stage2.VRW_SOURCE_RAM,
                                         MBlockSelector_stage3.VRW_VALUE_RAM,
                                         ALU.PASS_R)),
    ParserInstruction("STOREC", unit.Operand.DADDRESS, unit.Operand.CONSTANT,
                      EncodedInstruction(MBlockSelector_stage1.VR_SOURCE_CONST,
                                         MBlockSelector_stage2.VRW_SOURCE_RAM,
                                         MBlockSelector_stage3.VRW_VALUE_RAM,
                                         ALU.PASS_R)),
    ParserInstruction("CMP", unit.Operand.ADDRESS, unit.Operand.ADDRESS,
                      EncodedInstruction(MBlockSelector_stage1.VR_SOURCE_RAM,
                                         MBlockSelector_stage2.VRW_SOURCE_RAM,
                                         MBlockSelector_stage3.NO_WRITE,
                                         ALU.SUB)),
    ParserInstruction("CMPC", unit.Operand.ADDRESS, unit.Operand.CONSTANT,
                      EncodedInstruction(MBlockSelector_stage1.VR_SOURCE_CONST,
                                         MBlockSelector_stage2.VRW_SOURCE_RAM,
                                         MBlockSelector_stage3.NO_WRITE,
                                         ALU.SUB)),
    ParserInstruction("HLT", unit.Operand.CONSTANT, unit.Operand.CONSTANT,
                      EncodedInstruction(MBlockSelector_stage1.DONT_CARE,
                                         MBlockSelector_stage2.DONT_CARE,
                                         MBlockSelector_stage3.HLT,
                                         ALU.PASS_R)),
    ParserInstruction("JMP", unit.Operand.CONSTANT, unit.Operand.CONSTANT,
                      EncodedInstruction(MBlockSelector_stage1.VR_SOURCE_CONST,
                                         MBlockSelector_stage2.VR_SOURCE_SHL8_VRW_SOURCE_CONST,
                                         MBlockSelector_stage3.PC_NEXT,
                                         ALU.PASS_RW)),
    ParserInstruction("JMPM", unit.Operand.ADDRESS, unit.Operand.ADDRESS,
                      EncodedInstruction(MBlockSelector_stage1.VR_SOURCE_CONST,
                                         MBlockSelector_stage2.VR_SOURCE_SHL8_VRW_SOURCE_RAM,
                                         MBlockSelector_stage3.PC_NEXT,
                                         ALU.PASS_RW)),
    ParserInstruction("JZ", unit.Operand.CONSTANT, unit.Operand.CONSTANT,
                      EncodedInstruction(MBlockSelector_stage1.VR_SOURCE_CONST,
                                         MBlockSelector_stage2.VR_SOURCE_SHL8_VRW_SOURCE_CONST,
                                         MBlockSelector_stage3.PC_NEXT_IF_ZERO,
                                         ALU.PASS_RW)),
    ParserInstruction("JNZ", unit.Operand.CONSTANT, unit.Operand.CONSTANT,
                      EncodedInstruction(MBlockSelector_stage1.VR_SOURCE_CONST,
                                         MBlockSelector_stage2.VR_SOURCE_SHL8_VRW_SOURCE_CONST,
                                         MBlockSelector_stage3.PC_NEXT_IF_NOT_ZERO,
                                         ALU.PASS_RW)),
] + [
    ParserInstruction(ins_name, unit.Operand.ADDRESS, unit.Operand.ADDRESS,
                      EncodedInstruction(MBlockSelector_stage1.VR_SOURCE_RAM,
                                         MBlockSelector_stage2.VRW_SOURCE_RAM,
                                         MBlockSelector_stage3.VRW_SOURCE_RAM,
                                         alu_op))
    for ins_name, alu_op in [
        ("ADD", ALU.ADD),
        ("SUB", ALU.SUB),
        ("SHL", ALU.SHL),
        ("SHR", ALU.SHR),
        ("AND", ALU.AND),
        ("OR", ALU.OR),
        ("XOR", ALU.XOR),
    ]
] + [
    ParserInstruction(ins_name, unit.Operand.ADDRESS, unit.Operand.CONSTANT,
                      EncodedInstruction(MBlockSelector_stage1.VR_SOURCE_CONST,
                                         MBlockSelector_stage2.VRW_SOURCE_RAM,
                                         MBlockSelector_stage3.VRW_SOURCE_RAM,
                                         alu_op))
    for ins_name, alu_op in [
        ("ADDC", ALU.ADD),
        ("SUBC", ALU.SUB),
        ("SHLC", ALU.SHL),
        ("SHRC", ALU.SHR),
        ("ANDC", ALU.AND),
        ("ORC", ALU.OR),
        ("XORC", ALU.XOR),
    ]
]

def get_parser(name: str) -> ParserInstruction:
    name = name.upper()
    for ins in INSTRUCTIONS:
        if name == ins.name:
            return ins
    raise ValueError(f"Instruction parser for '{name}' not found")


def get_parsers_from_encoding(ins: EncodedInstruction) -> ParserInstruction:
    ans = []
    for _ins in INSTRUCTIONS:
        if _ins.encoded_instruction == ins:
            ans.append(_ins)
    return ans


def parse(name: str, tokens: List[Tuple[unit.Operand, unit.LazyLabel]]):
    # preprocess
    if name.upper() == "HLT":
        return [get_parser(name).parse([
            (unit.Operand.CONSTANT, unit.LazyLabel(util.LABEL_CONSTANT, 0)),
            (unit.Operand.CONSTANT, unit.LazyLabel(util.LABEL_CONSTANT, 0))
            ] + tokens)]

    if name.upper() == "JMP":
        assert len(tokens) == 1
        assert tokens[0][0] == unit.Operand.CONSTANT
        return [get_parser(name).parse([
            (unit.Operand.CONSTANT, tokens[0][1].bin_and(0xFF)),
            (unit.Operand.CONSTANT, tokens[0][1].shr(8))
            ])]

    if name.upper() == "JMPM":
        assert len(tokens) == 1
        assert tokens[0][0] == unit.Operand.ADDRESS
        return [get_parser(name).parse([
            (unit.Operand.ADDRESS, tokens[0][1].bin_and(0xFF)),
            (unit.Operand.ADDRESS, tokens[0][1].shr(8))
            ])]

    if name.upper() == "JZ" or name.upper() == "JNZ":
        assert len(tokens) == 1
        assert tokens[0][0] == unit.Operand.CONSTANT
        return [get_parser(name).parse([
            (unit.Operand.CONSTANT, tokens[0][1].bin_and(0xFF)),
            (unit.Operand.CONSTANT, tokens[0][1].shr(8))
            ])]

    # multi-step instructions
    if name == "PUSH":
        return [
            get_parser("SUBC").parse([
                (unit.Operand.ADDRESS, unit.LazyLabel(util.LABEL_CONSTANT, memory.ESP)),
                (unit.Operand.CONSTANT, unit.LazyLabel(util.LABEL_CONSTANT, 4))]),
            get_parser("STORE").parse([
                (unit.Operand.DADDRESS, unit.LazyLabel(util.LABEL_CONSTANT, memory.ESP)),
                ] + tokens)
            ]
    elif name == "POP":
        return [
            get_parser("LOAD").parse(tokens + [
                (unit.Operand.DADDRESS, unit.LazyLabel(util.LABEL_CONSTANT, memory.ESP)),
                ]),
            get_parser("ADDC").parse([
                (unit.Operand.ADDRESS, unit.LazyLabel(util.LABEL_CONSTANT, memory.ESP)),
                (unit.Operand.CONSTANT, unit.LazyLabel(util.LABEL_CONSTANT, 4))])
            ]
    elif name == "CALL":
        assert len(tokens) == 1, "call _jmp_address_"
        assert tokens[0][0] == unit.Operand.CONSTANT
        return [
            get_parser("PCPLUS").parse([
                (unit.Operand.ADDRESS, unit.LazyLabel(util.LABEL_CONSTANT, memory.MSI)),
                (unit.Operand.CONSTANT, unit.LazyLabel(util.LABEL_CONSTANT, 16))]),
            get_parser("SUBC").parse([
                (unit.Operand.ADDRESS, unit.LazyLabel(util.LABEL_CONSTANT, memory.ESP)),
                (unit.Operand.CONSTANT, unit.LazyLabel(util.LABEL_CONSTANT, 4))]),
            get_parser("STORE").parse([
                (unit.Operand.DADDRESS, unit.LazyLabel(util.LABEL_CONSTANT, memory.ESP)),
                (unit.Operand.ADDRESS, unit.LazyLabel(util.LABEL_CONSTANT, memory.MSI))
                ]),
            get_parser("JMP").parse([
                (unit.Operand.CONSTANT, tokens[0][1].bin_and(0xFF)),
                (unit.Operand.CONSTANT, tokens[0][1].shr(8))
                ])
            ]
    elif name == "RET":
        assert len(tokens) == 0
        return [
            get_parser("LOAD").parse([
                (unit.Operand.ADDRESS, unit.LazyLabel(util.LABEL_CONSTANT, memory.MSI)),
                (unit.Operand.DADDRESS, unit.LazyLabel(util.LABEL_CONSTANT, memory.ESP)),
                ]),
            get_parser("ADDC").parse([
                (unit.Operand.ADDRESS, unit.LazyLabel(util.LABEL_CONSTANT, memory.ESP)),
                (unit.Operand.CONSTANT, unit.LazyLabel(util.LABEL_CONSTANT, 4))]),
            get_parser("JMPM").parse([
                (unit.Operand.ADDRESS, unit.LazyLabel(util.LABEL_CONSTANT, memory.MSI)),
                (unit.Operand.ADDRESS, unit.LazyLabel(util.LABEL_CONSTANT, 0))
                ])
            ]

    return [get_parser(name).parse(tokens)]
