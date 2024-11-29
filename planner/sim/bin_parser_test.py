from planner.asm import program_parser
from planner.sim import bin_parser
from planner.sim import devices
from unittest import TestCase


PROGRAM = """
# Sample Program

PROGRAM_ORG equ 0x40
ADD_WITH equ 15

section .text
main:
    movc R2, ADD_WITH
    in   R4, 0x05
    add  R4, R2
    out 0x06, R4
loop_exit:
    jmp loop_exit
""".splitlines()

class BinParserTest(TestCase):

    def test_overall(self):
        asm = program_parser.AsmParser()
        for line in PROGRAM:
            asm.parse_line(line)
        binary_program = asm.get_str(resolved=True, rom_binary=True)

        _bin = bin_parser.BinRunner(binary_program)
        fake_input = devices.LatchInput("fake")
        fake_ouput = devices.Device()

        _bin.set_input_device(5, fake_input)
        _bin.set_output_device(6, fake_ouput)

        fake_input.set_input(56)
        for _ in range(100):
            _bin.step()
        self.assertEqual(fake_ouput.get(), 56+15)
