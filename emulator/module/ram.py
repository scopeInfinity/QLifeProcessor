import random

import specs

class RAM:

    def __init__(self, sz: int) -> None:
        self.mem = [random.random() for _ in range(sz)]
        self.max_sz = 1<<(specs.ADDRESS_LINES)
        assert sz <= self.max_sz, "address lines can't access full RAM of {sz} bytes"

    def read(self, address: int) -> int:
        assert address >= 0 and address < len(self.mem), "we don't encorage multiple address pointing to same memory location"
        return self.mem[address]

    def write(self, address: int, byte: int) -> None:
        assert address >= 0 and address < len(self.mem), "we don't encorage multiple address pointing to same memory location"
        assert byte >=0 and byte < 256
        self.mem[address] = byte
