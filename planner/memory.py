LABEL_PROGRAM_ORG = "PROGRAM_ORG"

# General Register R0,..R15
GENERAL_REGISTERS_COUNT = 8
def get_register_address(index):
    assert index >=0 and index < GENERAL_REGISTERS_COUNT
    return index*4

# Stack Registers
TOKEN_ESP = "ESP"
ESP = 0x20
ESB = 0x24

# free

# user program

DEFAULT_PROGRAM_ORG = 0x40
