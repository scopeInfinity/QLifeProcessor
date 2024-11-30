# TODO: This is not ready yet
#  Program
#       ROM[BootSequence]
#
#  Input devices required
#  * ROM[Program] output at 0
#  Output devices
#  * ROM[Program] address-line at 0
#  Really small program to copy ROM[Program] to RAM[Program]

PROGRAM_ORG equ 0x40

section .text
  main:
    # read metadata: program size
    movc R9, 0   # const -> ram
    out  0, R9   # ram -> io
    in   R0, 0   # io -> ram
    movc R8, 1

    movc R2, PROGRAM_ORG      # const -> ram
    movc R1, 1                # const -> ram
  _copy_more:
    out 0, R1                # ram -> io
    in  R3, 0                # io -> ram
    add R1, R8
    add R2, R8
    store [R2], R3             # ram -> ram
    # bytes left to copy
    subc R0, 1
    cmp R0, R9
    jz _copy_completed
    jmp _copy_more

  _copy_completed:
    jmp _copy_completed


