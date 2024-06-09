from enum import Enum
import inspect
from typing import List

from assembler.parser import Operand, InstructionTokens, TokenType

# Global parser map to instruction encoder
_PARSER_MAPPING = {}

class MBlockSelector(Enum):
    DONT_CARE = -1
    RAM = 0
    AUTO_BRAM = 1 # BROM is execute_from_brom else RAM
    IO = 2
    CONST = 3

    @staticmethod
    def wire(sel, do_not_care = None) -> List:
        if sel == MBlockSelector.DONT_CARE:
            assert do_not_care is not None
            sel = do_not_care
        assert sel.value >= 0 and sel.value < 4
        return [sel.value%2, sel.value>>1]

class ALU(Enum):
    ADD = 0
    SUB = 1
    SHL = 2
    SHR = 3
    LEFT = 4
    AND = 5
    OR = 6

    @staticmethod
    def wire(sel) -> List:
        assert sel.value >= 0 and sel.value < 8
        return [sel.value%2, (sel.value>>1)%2, sel.value>>2]

class EncodedInstruction:
    def __init__(self,
                mblock_selector1: MBlockSelector,
                mblock_selector2: MBlockSelector,
                alu_op: ALU,
                mblock_selector3: MBlockSelector,
                mblock_is_write: bool,
                update_program_counter: bool) -> None:
        self.mblock_selector1 = mblock_selector1
        self.mblock_selector2 = mblock_selector2
        self.alu_op = alu_op
        self.mblock_selector3 = mblock_selector3
        self.mblock_is_write = mblock_is_write
        self.update_program_counter = update_program_counter

    def encode(self):
        bits = [0]*32

        # bits[ 8:16] is address1
        # bits[16:24] is address2
        # bits[24:32] is address3

        # assign mblock_selector2 = 0b01
        # We assume mblock_selector2 to always be AUTO_BRAM.
        # Because an instruction meant it to be AUTO_BRAM or DONT_CARE.
        assert self.mblock_selector2 == MBlockSelector.AUTO_BRAM or (self.mblock_selector2 == MBlockSelector.DONT_CARE and self.alu_op == ALU.LEFT)

        # assign mblock_selector3[0] = 0
        # We assume mblock_selector3 to always be RAM or IO.
        # Because an instruction meant it to be RAM, IO or DONT_CARE.
        assert (
            self.mblock_selector3 == MBlockSelector.RAM or
            self.mblock_selector3 == MBlockSelector.IO or
            (self.mblock_selector3 == MBlockSelector.DONT_CARE and not self.mblock_is_write)
        )
        mblock_selector3_wire = MBlockSelector.wire(self.mblock_selector3, do_not_care=MBlockSelector.RAM)
        assert (
            MBlockSelector.wire(MBlockSelector.RAM, do_not_care=MBlockSelector.RAM)[1]^
            MBlockSelector.wire(MBlockSelector.IO, do_not_care=MBlockSelector.RAM)[1]) != 0b10, (
                "mselector only 1th bit is expected to be different for RAM and IO")

        bits[0:2] = MBlockSelector.wire(self.mblock_selector1)
        bits[2]   = mblock_selector3_wire[1]
        bits[3:6] = ALU.wire(self.alu_op)
        bits[6]   = self.update_program_counter
        bits[7]   = self.mblock_is_write

        # Tip: bits[8..16] is free for now

        return sum([bits[i]<<i for i in range(16)])

    def plug(self, a1, ar):
        self.a1 = a1
        # result address (ar) is same as a2
        # instructions like add reuses a2/ar as both input and result address
        self.ar = ar
        return self

    def encode_full(self) -> int:
        assert self.a1 is not None, "need a1 and ar for full instruction encoding"
        assert self.ar is not None, "need a1 and ar for full instruction encoding"
        return (self.encode()<<16) + (self.a1<<8) + (self.ar)


INSTRUCTIONS = {
    "IN": EncodedInstruction(MBlockSelector.IO, MBlockSelector.DONT_CARE, ALU.LEFT, MBlockSelector.RAM, True, False),
    "OUT":  EncodedInstruction(MBlockSelector.AUTO_BRAM, MBlockSelector.DONT_CARE, ALU.LEFT, MBlockSelector.IO, True, False),
    # CALL?
    # HLT?
    "MOV":  EncodedInstruction(MBlockSelector.AUTO_BRAM, MBlockSelector.DONT_CARE, ALU.LEFT, MBlockSelector.RAM, True, False),
    "MOVC":  EncodedInstruction(MBlockSelector.CONST, MBlockSelector.DONT_CARE, ALU.LEFT, MBlockSelector.RAM, True, False),
    "ADD":  EncodedInstruction(MBlockSelector.AUTO_BRAM, MBlockSelector.AUTO_BRAM, ALU.ADD, MBlockSelector.RAM, True, False),
    "SUB":  EncodedInstruction(MBlockSelector.AUTO_BRAM, MBlockSelector.AUTO_BRAM, ALU.SUB, MBlockSelector.RAM, True, False),
    "SHL":  EncodedInstruction(MBlockSelector.AUTO_BRAM, MBlockSelector.AUTO_BRAM, ALU.SHL, MBlockSelector.RAM, True, False),
    "SHR":  EncodedInstruction(MBlockSelector.AUTO_BRAM, MBlockSelector.AUTO_BRAM, ALU.SHR, MBlockSelector.RAM, True, False),
    "AND":  EncodedInstruction(MBlockSelector.AUTO_BRAM, MBlockSelector.AUTO_BRAM, ALU.AND, MBlockSelector.RAM, True, False),
    "OR":  EncodedInstruction(MBlockSelector.AUTO_BRAM, MBlockSelector.AUTO_BRAM, ALU.OR, MBlockSelector.RAM, True, False),

    "CMP":  EncodedInstruction(MBlockSelector.AUTO_BRAM, MBlockSelector.AUTO_BRAM, ALU.SUB, MBlockSelector.DONT_CARE, False, False),
    "JMP":  EncodedInstruction(MBlockSelector.CONST, MBlockSelector.DONT_CARE, ALU.LEFT, MBlockSelector.DONT_CARE, False, True),
    "JEQ":  EncodedInstruction(MBlockSelector.CONST, MBlockSelector.DONT_CARE, ALU.LEFT, MBlockSelector.DONT_CARE, False, True),
}

def generate_parser(instruction_fn, args_type: List[Operand]):
    def token_parser(tokens: InstructionTokens):
        if len(tokens.values) != len(args_type):
            raise ValueError(f"Invalid number of token for {tokens.name} instruction name")
        # Assert args_type and tokens type as same before calling
        for tok, arg_type in zip(tokens.values, args_type):
            if (tok[0] != arg_type):
                raise ValueError(f"Invalid arguments type provided in {tokens}")
        return instruction_fn(*[tok[1] for tok in tokens.values])
    return token_parser

def add_parser(*operand_types):
    def _add_parser(instruction_fn):
        def inner(*args):
            return instruction_fn(*args)

        args_name = inspect.getfullargspec(instruction_fn)
        print(f"{instruction_fn.__name__} has {args_name} as {operand_types}")
        # TODO: Limit compile time errors
        # assert len(args_name) == len(args)
        inner.parse = generate_parser(inner, operand_types)
        _PARSER_MAPPING[instruction_fn.__name__] = inner.parse
        return inner
    return _add_parser

@add_parser(Operand.ADDRESS, Operand.ADDRESS)
def IN(ram_address, input_address):
    return INSTRUCTIONS["IN"].plug(input_address, ram_address)

@add_parser(Operand.ADDRESS, Operand.ADDRESS)
def OUT(out_address: int, ram_address:int):
    return INSTRUCTIONS["OUT"].plug(ram_address, out_address)

@add_parser(Operand.ADDRESS, Operand.ADDRESS)
def MOV(dst:int, src: int):
    return INSTRUCTIONS["MOV"].plug(src, dst)

@add_parser(Operand.ADDRESS, Operand.CONSTANT)
def MOVC(dst:int, const: int):
    return INSTRUCTIONS["MOVC"].plug(const, dst)

@add_parser(Operand.ADDRESS, Operand.ADDRESS)
def ADD(dst:int, src: int):
    return INSTRUCTIONS["ADD"].plug(src, dst)

@add_parser(Operand.ADDRESS, Operand.ADDRESS)
def SUB(dst:int, src: int):
    return INSTRUCTIONS["SUB"].plug(src, dst)

@add_parser(Operand.ADDRESS, Operand.ADDRESS)
def SHL(dst:int, shift: int):
    return INSTRUCTIONS["SHL"].plug(shift, dst)

@add_parser(Operand.ADDRESS, Operand.ADDRESS)
def SHR(dst:int, shift: int):
    return INSTRUCTIONS["SHR"].plug(shift, dst)

@add_parser(Operand.ADDRESS, Operand.ADDRESS)
def AND(dst:int, src: int):
    return INSTRUCTIONS["AND"].plug(src, dst)

@add_parser(Operand.ADDRESS, Operand.ADDRESS)
def OR(dst:int, src: int):
    return INSTRUCTIONS["OR"].plug(src, dst)

@add_parser(Operand.ADDRESS, Operand.ADDRESS)
def CMP(src1: int, src2: int):
    return INSTRUCTIONS["CMP"].plug(src1, src2)

@add_parser(Operand.CONSTANT)
def JMP(location:int):
    return INSTRUCTIONS["JMP"].plug(location, 0)

@add_parser(Operand.CONSTANT)
def JEQ(location:int):
    return INSTRUCTIONS["JEQ"].plug(location, 0)

def parse(tokens: InstructionTokens):
    return _PARSER_MAPPING[tokens.name](tokens)