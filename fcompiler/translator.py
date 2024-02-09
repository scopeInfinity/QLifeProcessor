import sys
import logging
import re

logging.basicConfig(level=logging.INFO)

all_opcodes = dict(**{
    'leave': set(),
    'shl': set(),
    'addl': set(),
    'jne': set(),
    'imul': set(),
    'movaps': set(),
    'test': set(),
    'endbr64': set(),
    'nop': set(),
    'je': set(),
    'hlt': set(),
    'add': set(),
    'mov': set(),
    'idivl': set(),
    'jl': set(),
    'cltq': set(),
    'movzbl': set(),
    'cmp': set(),
    'movslq': set(),
    'jle': set(),
    'pop': set(),
    'movsbl': set(),
    'ret': set(),
    'call': set(),
    'and': set(),
    'push': set(),
    'sub': set(),
    'jmp': set(),
    'cmpl': set(),
    'lea': set(),
    'movl': set(),
    'cltd': set()
    }
)

def get_source():
    assert len(sys.argv) == 2, "program expect exactly one argument wit instruction filepath"
    return sys.argv[1]

def parse_toperand(opr: str):
    try:
        val = int(opr, 16)
        return "NUM"
    except ValueError:
        pass
    try:
        if opr.startswith("$0x"):
            val = int(opr[3:], 16)
            return "NUM"
        if opr.startswith("-0x"):
            val = -int(opr[3:], 16)
            return "NUM"
    except ValueError:
        pass
    if opr == r"%eax":
        return "AX"
    if opr == r"%ebx":
        return "BX"
    if opr == r"%ecx":
        return "CX"
    if opr == r"%edx":
        return "DX"
    if opr == r"%esi":
        return "SI"
    if opr == r"%edi":
        return "DI"
    if opr == r"%ebp":
        return "BP"
    if opr == r"%esp":
        return "SP"
    if opr == r"%ax":
        return "AX"
    if opr == r"%bx":
        return "BX"
    if opr == r"%cx":
        return "CX"
    if opr == r"%dx":
        return "DX"
    if opr == r"%si":
        return "SI"
    if opr == r"%di":
        return "DI"
    if opr == r"%bp":
        return "BP"
    if opr == r"%sp":
        return "SP"
    if opr == r"%al":
        return "AL"
    if opr == r"%bl":
        return "BL"
    if opr == r"%cl":
        return "CL"
    if opr == r"%dl":
        return "DL"
    if opr == r"%ah":
        return "AH"
    if opr == r"%bh":
        return "BH"
    if opr == r"%ch":
        return "CH"
    if opr == r"%dh":
        return "DH"


    raise Exception(f"don't know:'{opr}'")

def parse_toperand_simplify(oprs):
    return [o if o == "NUM" else "REG" for o in oprs]

def parse_toperands(oprs):
    operands = oprs.replace("(",",").replace(")",",").split(",")
    x = []
    for opr in operands:
        if opr:
            x.append(parse_toperand(opr))
    return parse_toperand_simplify(x)

def is_line_instruction(line):
    # being conservative
    assert "(bad)" not in line, "'bad' word found in the instructions, please verify."
    t_rest = line[3:]
    t_rest = re.sub("\s*(<|#).*", "", t_rest)
    if len(t_rest) == 0:
        raise ValueError
    try:
        t_address = int(line[:3], 16)
    except ValueError:
        raise ValueError # likely not an instruction line
    return (t_address, t_rest)

def parse_line(line_number, line):
    logging.debug("parsing line number: %d; %s", line_number, line)
    try:
        t_address, t_rest = is_line_instruction(line)
    except ValueError:
        logging.info("skipping not an instruction: %s", line)
        return # not an instruction
    tokens = t_rest.split()
    t_opcode = tokens[0]
    t_operands = tokens[1:]
    assert t_opcode in all_opcodes, f"translator doesn't understand '{t_opcode}' opcode"
    assert len(t_operands) <= 1, f"translator believes all opcode operands shouldn't be part of non-spaced chunk"

    print(t_address, t_opcode, t_operands)
    operands_type =  ()
    if len(t_operands) == 1:
        operands_type = tuple(parse_toperands(t_operands[0]))
    all_opcodes[t_opcode].add(operands_type)


def main():
    with open(get_source()) as f:
        lines = f.readlines()
        count = 0
        for line in lines:
            count += 1
            parse_line(count, line.rstrip())
    print(all_opcodes)

if __name__ == "__main__":
    main()