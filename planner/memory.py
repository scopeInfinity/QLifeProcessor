LABEL_PROGRAM_ORG = "PROGRAM_ORG"

# General Register R0,..R15
GENERAL_REGISTERS_COUNT = 8
TOKEN_GENERAL_REGISTERS = [f"R{i}" for i in range(0, GENERAL_REGISTERS_COUNT)]
def get_register_address(index):
    assert index >=0 and index < GENERAL_REGISTERS_COUNT
    return index*4

# Stack Registers
TOKEN_ESP = "ESP"
TOKEN_ESB = "ESB"
ESP = 0x20
ESB = 0x24
MSI = 0x28  # multi-step instruction state

# free

# boot sequence
BOOTSEQUENCE_LOAD = 0x30
BOOTSEQUENCE_ORG  = 0x34  # as we have 4-byte rom size header at top

# user program
DEFAULT_PROGRAM_ORG = 0x80
