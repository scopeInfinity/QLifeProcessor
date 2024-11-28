#   Program
#       Turn on/off the led corresponding to the button.
#
#   Chip
#       Button(s) with one end at in[0-2] with another end with
#       # pull down resister
#       [in0-button] [in1-button] [in2-button]
#       # Led(s) anode at out[0-2] and cathode at ground with some resister
#       [out0-led] [out1-button1] [out2-button2]

section .text
  main:
    MOVC R0, 0 # input source
    IN R1, R0
    OUT R0, R1
    jmp main
