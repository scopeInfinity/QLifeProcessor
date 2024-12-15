from planner.asm import program_parser
from planner.sim import bin_parser, devices, gui_devices
from threading import Thread
import pygame

PROGRAM_PATH = "programs/ping_pong.asm"

def step_runner(_bin):
    while True:
        _bin.step()

def start():
    asm = program_parser.AsmParser()
    with open(PROGRAM_PATH, "r") as f:
        asm.parse_lines(f.readlines())
    program_binary = asm.get_str(resolved=True, rom_binary=True)

    _bin = bin_parser.BinRunner(program_binary)
    gui_manager = gui_devices.GUIDeviceManager()


    input = devices.LatchInput("input", bits=4)
    gui_manager.add_device((0, 0), gui_devices.KeyPressedInput(input, {
            pygame.K_w: 0,
            pygame.K_s: 1,
            pygame.K_UP: 2,
            pygame.K_DOWN: 3,
        }))
    _bin.set_input_device(1, input)


    display = devices.LEDDisplay("LED", width_anode=16, height_cathode=8)
    gui_manager.add_device((0, 0), gui_devices.GUILed(display))
    _bin.set_output_device(6, display.get_anodes()[0])
    _bin.set_output_device(7, display.get_cathodes()[0])


    processor = Thread(None, step_runner, None, (_bin, ))
    processor.start()
    gui_manager.draw_loop()
