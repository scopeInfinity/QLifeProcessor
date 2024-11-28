from enum import Enum
from typing import List, Optional, Tuple

from assembler import unit, util

# # Global parser map to instruction encoder
# _PARSER_MAPPING = {}

class MBlockSelector(Enum):
    '''MBlockSelector defines the purpose of value_s[i].'''
    DONT_CARE = -1
    RAM = 0  # value[i] => RAM[value_s[i]]
    # TODO: Claim, we don't need AUTO_BRAM
    # We should never be reading any data from boot_ram. Any tiny miny data should be
    # part of instruction set as CONST.
    # AUTO_BRAM = 1 # value[i] => BROM[value_s[i]] is execute_from_brom else RAM
    IO = 2
    CONST = 3

    # TODO: What happens if we try to write on a CONST.

    @staticmethod
    def wire(sel, do_not_care = None) -> List:
        if sel == MBlockSelector.DONT_CARE:
            assert do_not_care is not None
            sel = do_not_care

        assert sel in [MBlockSelector.RAM, MBlockSelector.IO, MBlockSelector.CONST], "found: %s" % (sel)
        return [sel.value%2, sel.value>>1]

class ALU(Enum):
    ADD = 0
    SUB = 1
    SHL = 2
    SHR = 3
    PASS_R = 4
    AND = 5
    OR = 6

    @staticmethod
    def wire(sel) -> List:
        assert sel.value >= 0 and sel.value < 8
        return [sel.value%2, (sel.value>>1)%2, sel.value>>2]

class EncodedInstruction:
    def __init__(self,
                mblock_selector_r: MBlockSelector,
                mblock_selector_rw: MBlockSelector,
                alu_op: ALU,
                mblock_is_write: bool,
                update_program_counter: bool) -> None:
        self.mblock_selector_r = mblock_selector_r
        self.mblock_selector_rw = mblock_selector_rw
        self.alu_op = alu_op
        self.mblock_is_write = mblock_is_write
        self.update_program_counter = update_program_counter

        self.address_r = None
        self.address_rw = None


    def encode(self):
        # value_r  = &mblock_resolve(address_r)
        # value_rw = &mblock_resolve(address_rw)
        # value_rw = op(value_r, [value_rw])

        bits = [0]*32

        # Implemented in encode_full(...)
        # bits[16:24] is address_r (address to read only from)
        # bits[24:32] is address_rw (address to read from or write to)

        bits[0:2] = MBlockSelector.wire(self.mblock_selector_r)
        bits[2:4] = MBlockSelector.wire(self.mblock_selector_rw, do_not_care=MBlockSelector.CONST)
        bits[4:7] = ALU.wire(self.alu_op)[0:3]
        bits[7]   = self.update_program_counter
        bits[8]   = self.mblock_is_write

        return sum([bits[i]<<i for i in range(16)])

    def plug(self, address_rw: unit.LazyLabel, address_r: unit.LazyLabel):
        return FullyEncodedInstruction(self, address_rw, address_r)


class FullyEncodedInstruction:
    def __init__(self, encoded_instruction: EncodedInstruction, address_rw: unit.LazyLabel, address_r: unit.LazyLabel) -> None:
        self.address_rw = address_rw
        self.address_r = address_r
        self.encoded_instruction = encoded_instruction

    def get_binary(self, ensure_resolved=False) ->  List[unit.Data]:
        encoded = self.encoded_instruction.encode()
        return [
            unit.Data(encoded%256),
            unit.Data(encoded//256),
            unit.Data(self.address_r.get(ensure_resolved=ensure_resolved)),
            unit.Data(self.address_rw.get(ensure_resolved=ensure_resolved))
        ]

    def size(self):
        return 4  # bytes


class ParserInstruction:
    def __init__(self, name: str, type_rw: unit.Operand, type_r: unit.Operand, encoded_instruction: EncodedInstruction):
        self.name = name
        self.type_rw = type_rw
        self.type_r = type_r
        self.encoded_instruction = encoded_instruction

    def expects_operands(self):
        expects = []
        if self.type_rw != unit.Operand.IGNORE:
            expects.append(self.type_rw)
        if self.type_r != unit.Operand.IGNORE:
            expects.append(self.type_r)
        return expects

    def parse(self, values: List[Tuple[unit.Operand, int]]):
        return ParsedInstruction(self, values)

    def __str__(self) -> str:
        expects = ', '.join([str(x) for x in self.expects_operands()])
        return "%s %s" % (self.name, expects)


class ParsedInstruction:
    def __init__(self, _parser: ParserInstruction, values: List[Tuple[unit.Operand, unit.LazyLabel]]):
        self.parser = _parser
        self.values = values
        self.fully_encoded_instruction = self.get_fully_encoded_instruction(values)

    def get_fully_encoded_instruction(self, values: List[Tuple[unit.Operand, unit.LazyLabel]]):
        if self.parser.expects_operands() != [t[0] for t in values]:
            raise ValueError(f"{self.parser.name} want operand type {self.parser.expects_operands()}, given operand values {values}")
        values_index = 0
        if self.parser.type_rw != unit.Operand.IGNORE:
            address_rw = values[values_index][1]
            values_index+=1
        else:
            address_rw = unit.LazyLabel(util.LABEL_CONSTANT, 0)
        if self.parser.type_r != unit.Operand.IGNORE:
            address_r = values[values_index][1]
            values_index+=1
        else:
            address_r = unit.LazyLabel(util.LABEL_CONSTANT, 0)
        assert len(values) == values_index
        return self.parser.encoded_instruction.plug(address_rw, address_r)

    def get_str(self, resolved=False, binary=False):
        if binary:
            assert resolved
            return ''.join([x.get_str(binary=True) for x in self.fully_encoded_instruction.get_binary(ensure_resolved=True)])

        printable_values = []
        for val_type, val in self.values:
            assert val_type in [unit.Operand.ADDRESS, unit.Operand.CONSTANT]
            if val_type == unit.Operand.ADDRESS:
                printable_values.append("[%s]" % (val.get_str(resolved=resolved)))
            else:
                printable_values.append("%s" % (val.get_str(resolved=resolved)))
        return "%s %s" % (self.parser.name, ', '.join(printable_values))

    def __str__(self):
        return self.get_str(resolved=False, binary=False)

    def size(self):
        return self.fully_encoded_instruction.size()

INSTRUCTIONS = [
    ParserInstruction("IN", unit.Operand.ADDRESS, unit.Operand.ADDRESS, EncodedInstruction(MBlockSelector.IO, MBlockSelector.RAM, ALU.PASS_R, True, False)),
    ParserInstruction("OUT", unit.Operand.ADDRESS, unit.Operand.ADDRESS, EncodedInstruction(MBlockSelector.RAM, MBlockSelector.IO, ALU.PASS_R, True, False)),
    # CALL?
    # HLT?
    ParserInstruction("MOV", unit.Operand.ADDRESS, unit.Operand.ADDRESS,  EncodedInstruction(MBlockSelector.RAM, MBlockSelector.RAM, ALU.PASS_R, True, False)),
    ParserInstruction("MOVC", unit.Operand.ADDRESS, unit.Operand.CONSTANT,  EncodedInstruction(MBlockSelector.CONST, MBlockSelector.RAM, ALU.PASS_R, True, False)),
    ParserInstruction("ADD", unit.Operand.ADDRESS, unit.Operand.ADDRESS,  EncodedInstruction(MBlockSelector.RAM, MBlockSelector.RAM, ALU.ADD, True, False)),
    ParserInstruction("SUB", unit.Operand.ADDRESS, unit.Operand.ADDRESS,  EncodedInstruction(MBlockSelector.RAM, MBlockSelector.RAM, ALU.SUB, True, False)),
    ParserInstruction("SHL", unit.Operand.ADDRESS, unit.Operand.ADDRESS,  EncodedInstruction(MBlockSelector.RAM, MBlockSelector.RAM, ALU.SHL, True, False)),
    ParserInstruction("SHR", unit.Operand.ADDRESS, unit.Operand.ADDRESS,  EncodedInstruction(MBlockSelector.RAM, MBlockSelector.RAM, ALU.SHR, True, False)),
    ParserInstruction("AND", unit.Operand.ADDRESS, unit.Operand.ADDRESS,  EncodedInstruction(MBlockSelector.RAM, MBlockSelector.RAM, ALU.AND, True, False)),
    ParserInstruction("OR", unit.Operand.ADDRESS, unit.Operand.ADDRESS, EncodedInstruction(MBlockSelector.RAM, MBlockSelector.RAM, ALU.OR, True, False)),

    ParserInstruction("CMP", unit.Operand.ADDRESS, unit.Operand.ADDRESS,  EncodedInstruction(MBlockSelector.RAM, MBlockSelector.RAM, ALU.SUB, False, False)),
    ParserInstruction("JMP", unit.Operand.IGNORE, unit.Operand.CONSTANT,  EncodedInstruction(MBlockSelector.CONST, MBlockSelector.DONT_CARE, ALU.PASS_R, False, True)),
    ParserInstruction("JEQ", unit.Operand.IGNORE, unit.Operand.CONSTANT,  EncodedInstruction(MBlockSelector.CONST, MBlockSelector.DONT_CARE, ALU.PASS_R, False, True))
]

def get_parser(name: str) -> ParserInstruction:
    name = name.upper()
    for ins in INSTRUCTIONS:
        if name == ins.name:
            return ins
    raise ValueError(f"Instruction parser for '{name}' not found")
