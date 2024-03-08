from typing import List
import logging

from emulator import specs

class ROM:
    '''ROM is essential series of read-only bytes.

    We have two types of ROM
    * ROM[boot-sequence]
      * The smallest fixed program meant to copy ROM[program] into RAM.
      * Connects via static device in parallel to RAM for instruction read.
    * ROM[program]
      * Connects via flexible(?) input device

    ROM content is splitted into two parts (in-order)
    * metadata: program size [1-byte]
    * program: instructions and data

    It's upto `boot` module to understand the difference b/w
    the above parts and load content to RAM appropriately.
    '''
    def __init__(self, program_binary: str) -> None:
        self.program_bytes = self._build_program(program_binary)
        self.metadata_bytes = self._build_metadata(self.program_bytes)
        self.lbytes = self.metadata_bytes + self.program_bytes
        logging.info("ROM size: %d byte(s)", len(self.lbytes))

    def _build_program(self, content: str) -> List[int]:
        '''Returns list of byte(s).'''
        assert len(content) % 8 == 0
        assert set(content) <= set(['0', '1']), "only binary context is allowed"

        program_size = [int(content[8*i:8*(i+1)], 2) for i in range(len(content)//8)]
        return program_size

    def _build_metadata(self, program_bytes: List[int]):
        program_size = len(program_bytes)
        assert specs.ROM_MAXSIZE == 2**8, "we are dedicating only 1 byte for metadata"
        assert program_size > 0 and program_size < 2**8, f"program size upto {specs.ROM_MAXSIZE} bytes supported only"
        return [program_size]

