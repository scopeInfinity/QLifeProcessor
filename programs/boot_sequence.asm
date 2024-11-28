#  Program
#       ROM[BootSequence]
#
#  Input devices required
#  * ROM[Program] output at 0
#  Output devices
#  * ROM[Program] address-line at 0
#  Really small program to copy ROM[Program] to RAM[Program]

PROGRAM_START equ 0x20

section .text
  main:
    # read metadata: program size
    mov [R1], 0  # const -> ram
    OUT 0, [R1]  # ram -> io
    IN [R0], 0   # io -> ram

    mov [R2], PROGRAM_START  # const -> ram
    mov [R1], 1              # const -> ram
  _copy_more:
    OUT 0, [R1]              # ram -> io
    IN [R2], 0               # io -> ram
    add [R2], 1
    add [R1], 1
    # bytes left to copy
    sub [R0], 1
    cmp [R0], 0
    jneq _copy_more

  _copy_completed:
    jmp _copy_completed


