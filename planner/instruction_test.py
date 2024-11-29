from unittest import TestCase

from planner import instruction
from planner.asm import line_parser

class InstructionTest(TestCase):

    def test_all_instructions_validation(self):
        all_instructions_sample_list = [
            ("in R1, 20", "IN [1], 20"),
            ("out 10, R2", "OUT 10, [2]"),
            ("mov R3, R1", "MOV [3], [1]"),
            ("movc R4, 0x2", "MOVC [4], 2"),
            ("add R5, [35]", "ADD [5], [35]"),
            ("sub R6, [0x45]", "SUB [6], [69]"),
            ("shl R7, R1", "SHL [7], [1]"),
            ("shr R8, R1", "SHR [8], [1]"),
            ("and [0x32], R9", "AND [50], [9]"),
            ("or [0x12], [0x33]", "OR [18], [51]"),
            ("cmp R2, [33]", "CMP [2], [33]"),
            ("jmp 0x55", "JMP 85"),
            ("jeq 0x22", "JEQ 34"),
        ]

        instructions = set()
        for input_line, want in all_instructions_sample_list:
            name, tokens = line_parser.parse_line(input_line)
            self.assertIsNotNone(name)
            ins = instruction.get_parser(name).parse(tokens)
            self.assertEqual(want, str(ins))
            instructions.add(name)

        self.assertEqual(
            len(instructions),
            len(instruction.INSTRUCTIONS),
            msg="Sample instructions not provided for all instructions")



