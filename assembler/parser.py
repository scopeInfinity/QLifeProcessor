from enum import Enum
import re
from typing import List, Optional

class Operand(Enum):
    # Used as hardcoded values / addresses
    CONSTANT = 1  # mov [R0], 5
    # Used as variables storing some value at predefined memory location.
    ADDRESS = 2   # mov [R0], [10]
    # We don't have a concept of pointers yet.

class TokenType(Enum):
    INSTRUCTION = 1
    CONSTANT = 2
    ADDRESS = 3

class InstructionTokens:
    def __init__(self, name: str = None) -> None:
        self.name = name
        self.values = []

    def add(self, ttype: TokenType, value: int) -> None:
        # TODO: Resolve symbols
        if ttype == TokenType.CONSTANT:
            otype = Operand.CONSTANT
        elif ttype == TokenType.ADDRESS:
            otype = Operand.ADDRESS
        else:
            raise Exception(f"{ttype} is not supported as value")
        self.values.append((otype, value))

    def __str__(self) -> str:
        return f"[{self.name}: {self.values}]"

def parse_line(line: str) -> InstructionTokens:


    line = line.strip() + " "
    first_space = line.index(" ")
    instruction = line[:first_space].upper()
    tokens = InstructionTokens(instruction)

    # Parsing operands
    line = line[first_space:].strip()
    operands = line.split(",")
    for op in operands:
        op = op.strip()
        if len(op) == 0:
            raise ValueError(f"no-length operand found in {line}")
        if op.startswith("*"):
            optype = TokenType.ADDRESS
            op = op[1:].lstrip()
        else:
            optype = TokenType.CONSTANT
        try:
            value = int(op, 0)  # automatically understand base-10 and base-16
        except ValueError as e:
            raise ValueError(f"Invalid operand value {e} in {line}")
        tokens.add(optype, value)
    return tokens