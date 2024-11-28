from enum import Enum
import re
from typing import List, Tuple, Optional
from assembler import unit, util

# class Operand(Enum):
#     # Hardcoded values
#     # mov ..., 5
#     CONSTANT = 1
#     # Hardcoded address, can be thought as variable
#     # mov ..., [10]
#     # mov [10], ...
#     ADDRESS = 2
#     # We don't have a concept of pointers yet.

# class TokenType(Enum):
#     INSTRUCTION = 1
#     CONSTANT = 2
#     ADDRESS = 3


def parse_line(line: str) -> Tuple[Optional[str], Optional[List[Tuple[unit.Operand, unit.LazyLabel]]]]:
    try:
        comment_index = line.index("#")
        line = line[:comment_index]
    except ValueError:
        # no comments
        pass
    line = line.strip()
    if len(line) == 0:
        return (None, None)
    line = line + " "
    first_space = line.index(" ")
    instruction = line[:first_space].upper()

    tokens = []

    # Parsing operands
    line = line[first_space:].strip()
    operands = line.split(",")
    for op in operands:
        op = op.strip()
        if len(op) == 0:
            raise ValueError("no-length operand found in %s" % line)
        if op.startswith("R"):
            if len(op) != 2 or op[1] not in "0123456789":
                raise ValueError("Invalid mem-register {op} provided, only R0..R9 supported.")
            optype = unit.Operand.ADDRESS
            op = op[1:]
        elif op.startswith("[") and op.endswith("]"):
            optype = unit.Operand.ADDRESS
            op = op[1:-1].strip()
        else:
            optype = unit.Operand.CONSTANT
        try:
            value = unit.LazyLabel(util.LABEL_CONSTANT, int(op, 0))  # automatically understand base-10 and base-16
        except ValueError as e:
            if util.is_valid_label(op):
                value = unit.LazyLabel(op)
            else:
                raise ValueError(f"Invalid operand value '{str(e)}' in '{str(line)}'")
        tokens.append((optype, value))
    return (instruction, tokens)
