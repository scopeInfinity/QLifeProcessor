#   Program
#       Two Player Ping Pong Game
#
#   Controls
#       Up/Down button for each player
#       Game Reset button
#   Display (16*8)
#
#   X
#   X
#   X    O          X
#                   X
#                   X
#
#
#   Chip
#       H/W: 4+1 buttons, 2 8x8 LED matrix
#       OUT[0..7] = LED Matrix Row
#       OUT[8..15] = LED Matrix 1 Col
#       OUT[16..23] = LED Matrix 2 Col

# Input(1) = Numpad(0-7)
# Input(2) = Numpad(0-9)
# Output(6) = LED(width=16, low_is_enabled)
# Output(7) = LED(height=8, high_is_enabled)


PROGRAM_ORG equ 0x40

BAT_H    equ 3
BAT_MAXY equ 5
OUTPUT_WIDTH equ 6
OUTPUT_HEGHT equ 7
INPUT_DEVICE equ 1

section .text
  jmp main

section .data
    bat1_y    dd 2
    bat2_y    dd 2
    ball_x    dd 7
    ball_y    dd 2

section .text
  main:

  game:
    # call print
    jmp print
    game_after_print:
    jmp read_input_p1_up
    game_after_read:
    jmp sleep
    sleep_end:
    # only print, TODO: fix
    jmp game


    # call step
    # jmp step
    game_after_step:
    jmp game
    hlt_marker:
    jmp hlt_marker

  #wait_led_lit:
    # wait for 100 ins to let LED powered up
  #  mov [R0], 100
  #  _wait_led_lit_internal:
  #  sub [R0], 1
  #  cmp [R0], 0
  #  jneq _wait_led_lit_internal
  #  ret

  read_input_p1_up:
    IN R0, INPUT_DEVICE
    movc R1, 0x1
    and R1, R0
    jz read_input_p1_down
    subc [bat1_y], 1
  read_input_p1_down:
    movc R1, 0x02
    and R1, R0
    jz read_input_p2_up
    addc [bat1_y], 1
  read_input_p2_up:
    movc R1, 0x04
    and R1, R0
    jz read_input_p2_down
    subc [bat2_y], 1
  read_input_p2_down:
    movc R1, 0x08
    and R1, R0
    jz game_after_read
    addc [bat2_y], 1
    jmp game_after_read



  print:
    ## Player 1
    # anode col
    movc R0, 0x7F
    shlc R0, 8
    xorc R0, 0xFF
    # cathode row
    movc R1, 0x3
    shl R1, [bat1_y]
    OUT OUTPUT_WIDTH, R0
    OUT OUTPUT_HEGHT, R1

    jmp sleep2
    sleep_end2:
    ## Player 2
    # anode col
    movc R0, 0xFF
    shlc R0, 8
    xorc R0, 0xFE
    # cathode row
    movc R1, 0x3
    shl R1, [bat2_y]
    OUT OUTPUT_WIDTH, R0
    OUT OUTPUT_HEGHT, R1

    jmp game_after_print

  sleep:
   movc R0, 0xF0
   shlc R0, 2
   _sleep:
   subc R0, 1
   jz sleep_end
   jmp _sleep


  sleep2:
  movc R0, 0xF0
  shlc R0, 2
  _sleep2:
  subc R0, 1
  jz sleep_end2
  jmp _sleep2

section .text
  step:
    addc [ball_x], 1
    andc [ball_x], 0x07
    jmp game_after_step


