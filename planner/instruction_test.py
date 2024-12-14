from unittest import TestCase

from planner import instruction
from planner.asm import line_parser

class InstructionTest(TestCase):

    def test_all_instructions_validation(self):
        all_instructions_sample_list = [
            ("in R1, 20", "IN [4], 20"),
            ("out 10, R2", "OUT 10, [8]"),
            ("mov R3, R1", "MOV [12], [4]"),
            ("movc R4, 0x2", "MOVC [16], 2"),
            ("cmp R2, [33]", "CMP [8], [33]"),
            ("cmpc R6, 35", "CMPC [24], 35"),
            ("jmp 0x55, 0", "JMP 85, 0"),
            ("jmpm [0x55], [0]", "JMPM [85], [0]"),
            ("jz 0x22, 0", "JZ 34, 0"),
            ("jnz 0x22, 0", "JNZ 34, 0"),


            ("load R3, [R1]", "LOAD [12], [[4]]"),
            ("load R4, [[50]]", "LOAD [16], [[50]]"),
            ("store [R1], R3", "STORE [[4]], [12]"),
            ("store [[50]], R4", "STORE [[50]], [16]"),
            ("storec [[50]], 10", "STOREC [[50]], 10"),

            ("add  R0, [10]", "ADD  [0], [10]"),
            ("addc R1, 10",   "ADDC [4], 10"),
            ("sub  R2, [20]", "SUB  [8], [20]"),
            ("subc R3, 20",   "SUBC [12], 20"),
            ("shl  R4, [11]", "SHL  [16], [11]"),
            ("shlc R5, 11",   "SHLC [20], 11"),
            ("shr  R6, [12]", "SHR  [24], [12]"),
            ("shrc R7, 12",   "SHRC [28], 12"),
            ("and  R1, [50]", "AND  [4], [50]"),
            ("andc R2, 50",   "ANDC [8], 50"),
            ("or  R0, [65]",  "OR  [0], [65]"),
            ("orc R0, 65",    "ORC [0], 65"),
            ("xor  R1, [44]",  "XOR  [4], [44]"),
            ("xorc R1, 46",    "XORC [4],  46"),

            ("pcplus R0, 4",    "PCPLUS [0], 4"),
            ("hlt 0, 0",    "HLT 0, 0"),
        ]

        instructions = set()
        for input_line, want in all_instructions_sample_list:
            name, tokens = line_parser.parse_line(input_line)
            self.assertIsNotNone(name)
            ins = instruction.get_parser(name).parse(tokens)
            self.assertEqual(' '.join(want.split()), str(ins))
            instructions.add(name)

        self.assertEqual(
            len(instructions),
            len(instruction.INSTRUCTIONS),
            msg="Sample instructions not provided for all instructions")

    def test_multi_instructions(self):
        test_data = [
            ("hlt", ["HLT 0, 0"]),
            ("push R2", ["SUBC [32], 4", "STORE [[32]], [8]"]),
            ("pop R2", ["LOAD [8], [[32]]", "ADDC [32], 4"]),
        ]

        for input_line, want in test_data:
            name, tokens = line_parser.parse_line(input_line)
            self.assertIsNotNone(name)
            inss = instruction.parse(name, tokens)
            self.assertEqual(
                [' '.join(w.split()) for w in want],
                [str(ins) for ins in inss])

