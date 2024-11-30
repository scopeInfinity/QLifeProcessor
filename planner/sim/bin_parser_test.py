from planner.asm import program_parser
from planner.sim import bin_parser
from planner.sim import devices
from unittest import TestCase


PROGRAM = """
# Sample Program

PROGRAM_ORG equ 0x40

section .text
main:
    movc R1, 0

    # add array0+array1 to R1
    movc R2, array0
    load  R3, [R2]
    add R1, R3
    addc R2, 4
    load  R3, [R2]
    add R1, R3

    movc R2, 15
    # input(0x05)*15
    in   R4, 0x05
loop_start:
    cmpc R2, 0
    jz loop_end
    subc R2, 1
    add  R1, R4
    jmp loop_start
loop_end:
    out 0x06, R1
loop_exit:
    jmp loop_exit

section .data
array0 dd 31
array1 dd 24


""".splitlines()

class BinParserTest(TestCase):

    def test_overall(self):
        asm = program_parser.AsmParser()
        for line in PROGRAM:
            asm.parse_line(line)
        binary_program = asm.get_str(resolved=True, rom_binary=True)

        _bin = bin_parser.BinRunner(binary_program)
        fake_input = devices.LatchInput("fake", bits=32)
        fake_ouput = devices.Device(bits=32)

        _bin.set_input_device(5, fake_input)
        _bin.set_output_device(6, fake_ouput)

        fake_input.set_input(56)
        for _ in range(100):
            _bin.step()
        self.assertEqual(fake_ouput.get(), 31+24+56*15)
