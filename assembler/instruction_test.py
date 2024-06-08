from unittest import TestCase

from assembler import instruction
from assembler.parser import parse_line

class InstructionTest(TestCase):
    # TODO: Something is wrong!!! Test failing.
    # def test_instruction_binary_uniqueness(self):
    #     values = []
    #     for _, ins in instruction.INSTRUCTIONS.items():
    #         values.append(ins.encode())
    #     assert len(set(values)) == len(values)

    def test_instructions(self):
        ins = instruction.parse(parse_line("mov *10, *20"))
        ins.encode_full()

        ins = instruction.parse(parse_line("add *10, *20, *30"))
        ins.encode_full()

        ins = instruction.parse(parse_line("sub *10, *20, *40"))
        ins.encode_full()
