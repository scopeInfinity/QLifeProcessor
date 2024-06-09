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

    def test_all_instructions_validation(self):
        all_instructions_sample_list = [
            "in R1, *20",
            "out *10, R2",
            "mov R3, R1",
            "movc R4, 0x2",
            "add R5, *35",
            "sub R6, *0x45",
            "shl R7, R1",
            "shl R8, R1",
            "and *0x32, R9",
            "or *0x12, *0x33",
            "cmp R2, *33",
            "jmp 0x55",
            "jeq 0x22",
            ]
        for line in all_instructions_sample_list:
            instruction.parse(parse_line(line)).encode_full()
        self.assertEqual(
            len(all_instructions_sample_list),
            len(instruction.INSTRUCTIONS),
            msg="Sample instructions not provided for all instructions")