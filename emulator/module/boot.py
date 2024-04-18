from emulator.module.ram import RAM
from emulator.module.rom import ROM
from emulator.module.state_manager import StateManager


class Boot:
    def __init__(self, sm: StateManager, boot_rom: ROM, program_rom: ROM, ram: RAM) -> None:
        self.boot_rom = boot_rom
        self.program_rom = program_rom
        self.ram = ram
        self.state_manager = sm

    def button_reset_pressed(self):
        '''Trigger boot sequence.

        The function will keep running during the time
        button is pressed.

        The goal is to copy program_ROM into RAM.
        To acheive is execute ROM[boot] which essentially copies
        program_ROM connected as input_device into RAM.
        '''
        # TODO: how is this going to work?
        if not self.state_manager.read_from_bootrom:
            self.state_manager.pc = 0
            self.state_manager.read_from_bootrom = True

    def button_reset_nopressed(self):
        '''Reset to program execution state.

        Assumes button_reset_pressed was pressed long enough to
        complete execution of ROM[boot] which ends at infinite
        loop.
        '''
        self.state_manager.read_from_bootrom = False
