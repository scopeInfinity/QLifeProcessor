from unittest import TestCase

from planner.asm import line_parser
from planner import unit


class ParserTest(TestCase):

    def test_parse_line_success(self):
        name, tokens = line_parser.parse_line("mov [10], [20]")
        self.assertEqual(name, "MOV")
        self.assertEqual(tokens, [
            (unit.Operand.ADDRESS, 10),
            (unit.Operand.ADDRESS, 20)])

        name, tokens = line_parser.parse_line("movc [30], 0x15")
        self.assertEqual(name, "MOVC")
        self.assertEqual(tokens, [
            (unit.Operand.ADDRESS, 30),
            (unit.Operand.CONSTANT, 21)])

        name, tokens = line_parser.parse_line("jmp 10")
        self.assertEqual(name, "JMP")
        self.assertEqual(tokens, [
            (unit.Operand.CONSTANT, 10)])

        name, tokens = line_parser.parse_line("add [ 0x16 ] , [15 ]")
        self.assertEqual(name, "ADD")
        self.assertEqual(tokens, [
            (unit.Operand.ADDRESS, 22),
            (unit.Operand.ADDRESS, 15)])

    def test_parse_line_failures(self):
        with self.assertRaises(ValueError):
            line_parser.parse_line("mov [10],, [20]")
        with self.assertRaises(ValueError):
            line_parser.parse_line("mov [10], [[20]]")
        with self.assertRaises(ValueError):
            line_parser.parse_line("mov 10 10")
