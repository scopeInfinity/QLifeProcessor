# TODO: This is not ready yet
#  Program
#       ROM[BootSequence]
#
#  Input devices required at 0x0
#  * address
#  Output devices
#  * PROGRAM_ROM[address] at 0x0
#  Really small program to copy ROM[Program] to RAM[Program]

PROGRAM_ORG equ 0x80
PROGRAM_DEST equ 0x40

ROM_INPUT_VALUE equ 0x0
ROM_OUTPUT_ADDRESS  equ 0x0

section .text
  main:
    # read metadata: program size
    # assume size mod 4 = 0
    movc R0, 0
    out  0x10, R0
    in   R0, ROM_INPUT_VALUE
    movc R5, 0

    movc R1, 1
    movc R2, PROGRAM_DEST
  _copy_more:
    out 0x10, R1
    in  R3, 0x20
    store [R2], R3
    addc R2, 4
    addc R1, 4
    subc R0, 4

    cmp R0, R5

    # jmp to program if copy is completed
    jz PROGRAM_DEST

    jmp _copy_more

