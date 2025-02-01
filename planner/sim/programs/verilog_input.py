from planner.sim import verilog_devices, gui_devices
from planner.sim import devices, gui_devices
import pygame

def start():
    io = verilog_devices.VerilogIO()
    gui_manager = gui_devices.GUIDeviceManager()

    input = devices.LatchInput("input", bits=4)
    gui_manager.add_device((0, 0), gui_devices.KeyPressedInput(input, {
            pygame.K_w: 0,
            pygame.K_s: 1,
            pygame.K_UP: 2,
            pygame.K_DOWN: 3,
        }))
    io.set_input_device(1, input)

    display = devices.LEDDisplay("LED", use_print=False, width_anode=16, height_cathode=8)
    gui_manager.add_device((0, 0), gui_devices.GUILed(display))
    io.set_output_device(6, display.get_anodes()[0])
    io.set_output_device(7, display.get_cathodes()[0])
    io.run(blocking=False)
    gui_manager.draw_loop()
