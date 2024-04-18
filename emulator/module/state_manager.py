class StateManager:
    def __init__(self) -> None:
        self._read_from_bootrom = False

    @property
    def read_from_bootrom(self):
        '''Should instructions from boot_rom instead of RAM'''
        return self.read_from_bootrom

    @read_from_bootrom.setter
    def read_from_bootrom(self, val: bool):
        self.read_from_bootrom = val
