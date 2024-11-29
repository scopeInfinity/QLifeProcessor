#   Program
#       Turn on/off the led corresponding to the button.
#
#   Chip
#       Button(s) with one end at input_device[5][pin:0..2] with another end with
#       # pull down resister
#       [in0-button] [in1-button] [in2-button]
#       # Led(s) anode at out[0-2] and cathode at ground with some resister
#       [out0-led] [out1-button1] [out2-button2]
#       at output_device[6][pin:0..2]

PROGRAM_ORG equ 0x40

section .text
  main:
    IN R1, 5
    OUT 6, R1
    jmp main
