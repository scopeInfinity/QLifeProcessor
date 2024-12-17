from planner.asm import program_parser
from planner.sim import bin_parser, devices, gui_devices
from threading import Thread
import pygame

BOOTSEQUENCE_PATH = "programs/boot_sequence.asm"
PROGRAM_PATH = "programs/ping_pong.asm"

def step_runner(_bin):
    while True:
        _bin.step()

def get_asm_binary(fname: str):
    asm = program_parser.AsmParser()
    with open(fname, "r") as f:
        asm.parse_lines(f.readlines())
    return asm.get_str(resolved=True, rom_binary=True)


def start():
    bsrom_binary = get_asm_binary(BOOTSEQUENCE_PATH)
    program_binary = get_asm_binary(PROGRAM_PATH)

    _bin = bin_parser.BinRunner(bsrom_binary)
    gui_manager = gui_devices.GUIDeviceManager()

    prom = devices.ProgramROM("prom", program_binary)
    _bin.set_output_device(2, prom.address_line)
    _bin.set_input_device(2, prom.value_line)

    input = devices.LatchInput("input", bits=4)
    gui_manager.add_device((0, 0), gui_devices.KeyPressedInput(input, {
            pygame.K_w: 0,
            pygame.K_s: 1,
            pygame.K_UP: 2,
            pygame.K_DOWN: 3,
        }))
    _bin.set_input_device(1, input)


    display = devices.LEDDisplay("LED", use_print=False, width_anode=16, height_cathode=8)
    gui_manager.add_device((0, 0), gui_devices.GUILed(display))
    _bin.set_output_device(6, display.get_anodes()[0])
    _bin.set_output_device(7, display.get_cathodes()[0])


    processor = Thread(None, step_runner, None, (_bin, ))
    processor.start()
    gui_manager.draw_loop()
