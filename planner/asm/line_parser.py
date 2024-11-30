from typing import List, Tuple, Optional
from planner import unit, util

def address_of(op: unit.Operand):
    if op == unit.Operand.CONSTANT:
        return unit.Operand.ADDRESS
    if op == unit.Operand.ADDRESS:
        return unit.Operand.DADDRESS
    raise AssertionError("can't take address of %s" % op)

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
        optype = unit.Operand.CONSTANT
        if op.startswith("[") and op.endswith("]"):
            optype = address_of(optype)
            op = op[1:-1].strip()
        if op.startswith("[") and op.endswith("]"):
            optype = address_of(optype)
            op = op[1:-1].strip()

        if op.startswith("R"):
            if len(op) != 2 or op[1] not in "0123456789":
                raise ValueError("Invalid mem-register {op} provided, only R0..R9 supported.")
            optype = address_of(optype)
            op = str(int(op[1:])*4)

        try:
            value = unit.LazyLabel(util.LABEL_CONSTANT, int(op, 0))  # automatically understand base-10 and base-16
        except ValueError as e:
            if util.is_valid_label(op):
                value = unit.LazyLabel(op)
            else:
                raise ValueError(f"Invalid operand value '{str(e)}' in '{str(line)}'")
        tokens.append((optype, value))
    return (instruction, tokens)
