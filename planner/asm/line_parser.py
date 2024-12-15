from typing import List, Tuple, Optional
from planner import unit, util, memory

def address_of(op: unit.Operand):
    if op == unit.Operand.CONSTANT:
        return unit.Operand.ADDRESS
    if op == unit.Operand.ADDRESS:
        return unit.Operand.DADDRESS
    raise AssertionError("can't take address of %s" % op)

def parse_line(line: str) -> Tuple[Optional[str], Optional[List[Tuple[unit.Operand, unit.LazyLabel]]]]:
    orginal_line = line
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
    if len(line) == 0:
        # no operand
        operands = []
    else:
        operands = line.split(",")
    for op in operands:
        op = op.strip()
        if len(op) == 0:
            raise ValueError("no-length operand found in '%s'" % orginal_line)
        optype = unit.Operand.CONSTANT
        if op.startswith("[") and op.endswith("]"):
            optype = address_of(optype)
            op = op[1:-1].strip()
        if op.startswith("[") and op.endswith("]"):
            optype = address_of(optype)
            op = op[1:-1].strip()

        if op.upper() == memory.TOKEN_ESP:
            optype = address_of(optype)
            op = str(memory.ESP)
        if op.upper() == memory.TOKEN_ESB:
            optype = address_of(optype)
            op = str(memory.ESB)
        elif op in memory.TOKEN_GENERAL_REGISTERS:
            optype = address_of(optype)
            try:
                rindex = int(op[1:])
            except ValueError as e:
                raise ValueError(f"Invalid mem-register {op} provided, only R0..R{memory.GENERAL_REGISTERS_COUNT-1} supported: {e}")
            op = str(memory.get_register_address(rindex))
        try:
            int_val = int(op, 0)
            value = unit.LazyLabel(util.LABEL_CONSTANT, int_val)  # automatically understand base-10 and base-16
        except ValueError as e:
            if util.is_valid_label(op):
                value = unit.LazyLabel(op)
            else:
                raise ValueError(f"Invalid operand value '{str(e)}' in '{str(line)}'")
        tokens.append((optype, value))
    return (instruction, tokens)
