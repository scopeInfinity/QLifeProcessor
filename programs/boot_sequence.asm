#  Program
#       ROM[BootSequence]
#  Small program to copy PROM[1+i] to RAM[org+i]
#
# output(2) = PROGRAM_ROM address line
PROM_ADDRESS_LINE equ 2
# input(2) = PROGRAM_ROM value
PROM_VALUE_LINE equ 2

PROGRAM_ORG equ 0x30
RAM_PROGRAM_ORG equ 0x80

ROM_INPUT_VALUE equ 0x0
ROM_OUTPUT_ADDRESS  equ 0x0

section .text
  main:
    # read metadata: program size
    # assume size mod 4 = 0
    movc R0, 0
    out  PROM_ADDRESS_LINE, R0
    in   R0, PROM_VALUE_LINE
    shrc R0, 2

    movc R1, 4
    movc R2, RAM_PROGRAM_ORG
  copy_more:
    cmpc R0, 0
    jz copy_completed
    out  PROM_ADDRESS_LINE, R1
    in R3, PROM_VALUE_LINE
    store [R2], R3
    addc  R2, 4
    addc  R1, 4
    subc  R0, 1
    jmp copy_more

  copy_completed:
    jmp RAM_PROGRAM_ORG
