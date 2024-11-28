from unittest import TestCase

from assembler import asm_parser

PROGRAM = """
# Sample Program

TOTAL equ 0x10

section .text
main:
    movc R1, 0
    movc R2, TOTAL
    movc R3, 1
loop:
    cmp R1, R2
    jeq loop_exit
    add R1, R3
    mov [last_value], R1
    out [0x00], R1
    jmp loop
loop_exit:
    jmp loop_exit

section .data
last_value db 0

""".splitlines()

class AsmParserTest(TestCase):

    def test_asm_parser_binary(self):
        asm = asm_parser.AsmParser()
        for line in PROGRAM:
            asm.parse_line(line)
        output = asm.get_str(resolved=True, rom_binary=True)

    def test_asm_parser_unresolved(self):
        asm = asm_parser.AsmParser()
        for line in PROGRAM:
            asm.parse_line(line)
        output = asm.get_str(resolved=False, rom_binary=False)

    def test_asm_parser_resolved(self):
        asm = asm_parser.AsmParser()
        for line in PROGRAM:
            asm.parse_line(line)
        output = asm.get_str(resolved=True, rom_binary=False)

