from planner.asm import program_parser
from planner.sim import bin_parser
from planner.sim import devices
from planner import util, memory
from unittest import TestCase
from typing import List


def get_asm_binary_from_lines(lines: List[str]):
    asm = program_parser.AsmParser()
    asm.parse_lines(lines)
    return asm.get_str(resolved=True, rom_binary=True)

def get_asm_binary_from_file(fname: str):
    with open(fname, "r") as f:
        return get_asm_binary_from_lines(f.readlines())


class BinParserTest(TestCase):
    FAKE_INPUT_AT = 0x05
    FAKE_OUPUT_AT = 0x06

    def setUp(self) -> None:
        self.clock = devices.Clock()
        ram = devices.RAM()

        bsrom_binary = get_asm_binary_from_file(util.BOOTSEQUENCE_PATH)
        brom = devices.ROM("brom", bsrom_binary)

        self.fake_input = devices.LatchInput("fake", bits=32)
        self.fake_ouput = devices.Device(bits=32)

        self.bin = bin_parser.BinRunner(self.clock, ram, brom)
        self.bin.set_input_device(self.FAKE_INPUT_AT, self.fake_input)
        self.bin.set_output_device(self.FAKE_OUPUT_AT, self.fake_ouput)


    def execute(self, program: str):
        program_binary = get_asm_binary_from_lines(program.splitlines())

        prom = devices.ROM("prom", program_binary)
        self.bin.set_output_device(2, prom.address_line)
        self.bin.set_input_device(2, prom.value_line)

        self.clock.start()
        while self.bin.is_power_on():
            pass
        # wait for hlt
        self.clock.stop()

    def get_ram_byte(self, address: int):
        return self.bin.read_ram(address, 4)[0]

    def test_io(self):
        self.fake_input.set_input(10)
        self.execute(f"""
            PROGRAM_ORG equ {memory.DEFAULT_PROGRAM_ORG}
            section .text
            main:
                in R0, {self.FAKE_INPUT_AT}
                out {self.FAKE_OUPUT_AT}, R0
                hlt
        """)
        self.assertEqual(self.fake_ouput.get(), 10)

    def test_mov(self):
        self.execute(f"""
            PROGRAM_ORG equ {memory.DEFAULT_PROGRAM_ORG}
            section .text
            main:
                movc R0, 0x45
                mov  R1, R0
                out {self.FAKE_OUPUT_AT}, R1
                hlt
        """)
        self.assertEqual(self.fake_ouput.get(), 0x45)


    def test_simple_alu(self):
        self.execute(f"""
            PROGRAM_ORG equ {memory.DEFAULT_PROGRAM_ORG}
            section .text
            main:
                movc R0, 1
                movc R1, 2
                movc R2, 2
                movc R3, 5
                movc R4, 5
                movc R5, 7
                movc R6, 7
                add R1, R0
                sub R2, R0
                shl R3, R0
                shr R4, R0
                or  R5, R0
                xor R6, R0
                hlt
        """)
        expect = [
            (4, 3),
            (8, 1),
            (12, 10),
            (16, 2),
            (20, 7),
            (24, 6)
        ]

        for address, value in expect:
            self.assertEqual(self.get_ram_byte(address), value)

    def test_simple_aluc(self):
        self.execute(f"""
            PROGRAM_ORG equ {memory.DEFAULT_PROGRAM_ORG}
            section .text
            main:
                movc R1, 9
                movc R2, 9
                movc R3, 9
                movc R4, 9
                movc R5, 9
                movc R6, 9
                addc R1, 10
                subc R2, 5
                shlc R3, 3
                shrc R4, 2
                orc  R5, 3
                xorc R6, 3
                hlt
        """)
        expect = [
            (4, 19),
            (8, 4),
            (12, 72),
            (16, 2),
            (20, 11),
            (24, 10)
        ]

        for address, value in expect:
            self.assertEqual(self.get_ram_byte(address), value)

    def test_stack(self):
        self.fake_input.set_input(45)
        self.execute(f"""
            PROGRAM_ORG equ {memory.DEFAULT_PROGRAM_ORG}

            section .text
            main:
                movc ESP, 0xFC
                in R0, {self.FAKE_INPUT_AT}
                push R0
                pop R1
                out {self.FAKE_OUPUT_AT}, R1
                hlt
        """)
        self.assertEqual(self.fake_ouput.get(), 45)

    def test_jmp(self):
        self.fake_input.set_input(45)
        self.execute(f"""
            PROGRAM_ORG equ {memory.DEFAULT_PROGRAM_ORG}

            section .text
            main:
                in R0, {self.FAKE_INPUT_AT}
                cmpc R0, 10 # incorrect
                jz bad
                cmpc R0, 45 # correct
                jz good1
                jmp bad

            good1:
                movc R1, 45
                cmp R0, R1 # correct
                jnz bad
                movc R1, 10
                cmp R0, R1 # incorrect
                jnz good2
                jmp bad

            good2:
                jmp good3
                hlt

            good3:
                movc R1, all_good
                jmpm R1

            bad:
                hlt
            all_good:
                out {self.FAKE_OUPUT_AT}, R0
                hlt
        """)
        self.assertEqual(self.fake_ouput.get(), 45)


    def test_data_section(self):
        self.execute(f"""
            PROGRAM_ORG equ {memory.DEFAULT_PROGRAM_ORG}
            section .text
            main:
                shlc [array_0], 2
                mov R0, [array_0]
                mov R1, [array_1]
                mov R2, [array_2]
                add R0, R1
                add R0, R2
                out {self.FAKE_OUPUT_AT}, R0
                hlt

            section .data
                array_0 dd 11
                array_1 dd 22
                array_2 dd 30
        """)
        self.assertEqual(self.fake_ouput.get(), 96)

    def test_bss_section(self):
        self.execute(f"""
            PROGRAM_ORG equ {memory.DEFAULT_PROGRAM_ORG}
            section .text
            main:
                movc R0, array_end
                subc R0, array_start
                out {self.FAKE_OUPUT_AT}, R0
                hlt

            section .bss
                array_start: resb 4
                resb 6
                array_end:
        """)
        self.assertEqual(self.fake_ouput.get(), 10)

    def test_load_store(self):
        self.execute(f"""
            PROGRAM_ORG equ {memory.DEFAULT_PROGRAM_ORG}
            section .text
            main:
                movc [array_ptr], array_0
                load R0, [[array_ptr]]
                addc [array_ptr], 4

                store [[array_ptr]], R0
                mov R1, [array_1]
                storec [[array_ptr]], 10
                add R1, [array_1]

                out {self.FAKE_OUPUT_AT}, R1
                hlt

            section .data
                array_0 dd 15
            section .bss
                array_1: resb 4
                array_ptr: resb 4
                array_end:
        """)
        self.assertEqual(self.fake_ouput.get(), 25)

    def test_call(self):
        self.fake_input.set_input(45)
        self.execute(f"""
            PROGRAM_ORG equ {memory.DEFAULT_PROGRAM_ORG}

            section .text
            main:
                movc ESP, 0xFC
                movc R1, 10
                movc R2, 15
                call sum
                jmp end
                hlt  # guard bad marker

            sum:
                push R1
                add R1, R2
                mov R0, R1
                pop R1
                ret
                hlt  # guard bad marker

            end:
                out {self.FAKE_OUPUT_AT}, R0
                hlt
        """)
        self.assertEqual(self.fake_ouput.get(), 25)
