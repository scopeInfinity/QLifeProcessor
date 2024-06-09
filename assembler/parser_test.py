from unittest import TestCase

from assembler.parser import parse_line, Operand

class ParserTest(TestCase):

    def test_parse_line_success(self):
        tokens = parse_line("mov *10, *20")
        self.assertEqual(tokens.name, "MOV")
        self.assertEqual(tokens.values, [
            (Operand.ADDRESS, 10),
            (Operand.ADDRESS, 20)])


        tokens = parse_line("movc *30, 0x15")
        self.assertEqual(tokens.name, "MOVC")
        self.assertEqual(tokens.values, [
            (Operand.ADDRESS, 30),
            (Operand.CONSTANT, 21)])


        tokens = parse_line("jmp 10")
        self.assertEqual(tokens.name, "JMP")
        self.assertEqual(tokens.values, [
            (Operand.CONSTANT, 10)])


        tokens = parse_line("add * 0x16 , *15")
        self.assertEqual(tokens.name, "ADD")
        self.assertEqual(tokens.values, [
            (Operand.ADDRESS, 22),
            (Operand.ADDRESS, 15)])

    def test_parse_line_failures(self):
        with self.assertRaises(ValueError):
            parse_line("mov *10,, *20")
        with self.assertRaises(ValueError):
            parse_line("mov *10, **20")
        with self.assertRaises(ValueError):
            parse_line("mov *10, AB")
        with self.assertRaises(ValueError):
            parse_line("mov 10 10")
