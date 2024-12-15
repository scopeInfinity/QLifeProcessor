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

BALL_STEP_SIZE equ 2
GAME_OVER_BLINK_STEP equ 5

BALL_DIR_RIGHT    equ 1
BALL_DIR_LEFT     equ 2
# BALL_DIR_RIGHT|BALL_DIR_LEFT
BALL_DIR_FLIP_HOR equ 3
# if not up or down, ball goes horizontally
BALL_DIR_UP       equ 4
BALL_DIR_DOWN     equ 8
# BALL_DIR_UP|BALL_DIR_DOWN
BALL_DIR_FLIP_VER equ 12

BALL_MAXX equ 14
BALL_MINX equ 1
BALL_MAXY equ 7
BALL_MINY equ 0


section .text
  main:
    movc ESP, 0xFF
    shlc ESP, 8
    orc ESP, 0xF0
    jmp game

section .data
    bat1_y    dd 2
    bat2_y    dd 2
    ball_x    dd 7
    ball_y    dd 2
    mask16f   dd 0xFFFF
    ball_step_counter dd 0
    ball_dir  dd 6

    game_over_blink_counter dd 0
    game_over_blink dd 1

section .text
  game:
    call print
    call read_input_p1_up
    call step
    jmp game

  game_over:
    call game_over_step
    call print
    jmp game_over

  game_over_step:
    cmpc [game_over_blink_counter], 0
    jnz _game_over_step_end
    xorc [game_over_blink], 1
    movc [game_over_blink_counter], GAME_OVER_BLINK_STEP
  _game_over_step_end:
    subc [game_over_blink_counter], 1
    ret


  read_input_p1_up:
    IN R0, INPUT_DEVICE
    movc R1, 0x1
    and R1, R0
    jz read_input_p1_down
    cmpc [bat1_y], 0
    jz read_input_p1_down
    subc [bat1_y], 1
  read_input_p1_down:
    movc R1, 0x02
    and R1, R0
    jz read_input_p2_up
    cmpc [bat1_y], BAT_MAXY
    jz read_input_p2_up
    addc [bat1_y], 1
  read_input_p2_up:
    movc R1, 0x04
    and R1, R0
    jz read_input_p2_down
    cmpc [bat2_y], 0
    jz read_input_p2_down
    subc [bat2_y], 1
  read_input_p2_down:
    movc R1, 0x08
    and R1, R0
    jz read_input_end
    cmpc [bat2_y], BAT_MAXY
    jz read_input_end
    addc [bat2_y], 1
  read_input_end:
    ret

  print:
    # if game over draw blink bat animation
    cmpc [game_over_blink], 0
    jz _draw_ball

    ## Player 1
    # anode col
    movc R0, 0x7F
    shlc R0, 8
    xorc R0, 0xFF
    # cathode row
    movc R1, 0x7
    shl R1, [bat1_y]
    OUT OUTPUT_WIDTH, R0
    OUT OUTPUT_HEGHT, R1
    call sleep

    ## Player 2
    # anode col
    movc R0, 0xFF
    shlc R0, 8
    xorc R0, 0xFE
    # cathode row
    movc R1, 0x7
    shl R1, [bat2_y]
    OUT OUTPUT_WIDTH, R0
    OUT OUTPUT_HEGHT, R1
    call sleep

  _draw_ball:
    ## Ball
    mov R0, [ball_x]
    movc R1, 0x80
    shlc R1, 8
    shr R1, R0
    xor R1, [mask16f]
    mov R0, [ball_y]
    movc R2, 1
    shl R2, R0
    OUT OUTPUT_WIDTH, R1
    OUT OUTPUT_HEGHT, R2
    call sleep

    ret

  sleep:
    movc R0, 0xF0
    shlc R0, 1
    _sleep:
    subc R0, 1
    jnz _sleep
    ret

  step:
    cmpc [ball_step_counter], 0
    jnz step_over
    movc [ball_step_counter], BALL_STEP_SIZE
    call step_ball_move
  step_over:
    subc [ball_step_counter], 1
    ret

  step_ball_move:
    cmpc [ball_x], BALL_MAXX
    jz _step_ball_collision_hor_right
    cmpc [ball_x], BALL_MINX
    jz _step_ball_collision_hor_left
  _step_ball_collision_hor_over:
    cmpc [ball_y], BALL_MAXY
    jz _step_ball_collision_ver
    cmpc [ball_y], BALL_MINY
    jz _step_ball_collision_ver
  _step_ball_collision_ver_over:

    mov R0, [ball_dir]
    andc R0, BALL_DIR_RIGHT
    jz _step_ball_left
    # move_right
    addc [ball_x], 1
    jmp _step_ball_up
  _step_ball_left:
    # move left
    subc [ball_x], 1
  _step_ball_up:
    mov R0, [ball_dir]
    andc R0, BALL_DIR_UP
    jz _step_ball_down
    # move up
    subc [ball_y], 1
  _step_ball_down:
    mov R0, [ball_dir]
    andc R0, BALL_DIR_DOWN
    jz _step_ball_move_over
    # move down
    addc [ball_y], 1
  _step_ball_move_over:
    ret

  _step_ball_collision_hor_right:
    push [bat2_y]
    call _step_ball_collision_hor
    pop R7
    jmp _step_ball_collision_hor_over

  _step_ball_collision_hor_left:
    push [bat1_y]
    call _step_ball_collision_hor
    pop R7
    jmp _step_ball_collision_hor_over

  _step_ball_collision_hor:
    # Argument
    # bat_y
    mov esb, esp
    addc esb, 4
    load R1, [esb] # bat_y

    xorc [ball_dir], BALL_DIR_FLIP_HOR
    movc R0, BALL_DIR_FLIP_VER
    xorc R0, 0xFF
    and [ball_dir], R0
    cmp [ball_y], R1
    jz _step_ball_collision_hor_right_go_up
    addc R1, 1
    cmp [ball_y], R1
    jz _step_ball_collision_hor_right_go_hor
    addc R1, 1
    cmp [ball_y], R1
    jz _step_ball_collision_hor_right_go_down
    jmp game_over
  _step_ball_collision_hor_right_go_up:
    orc [ball_dir], BALL_DIR_UP
    ret
  _step_ball_collision_hor_right_go_down:
    orc [ball_dir], BALL_DIR_DOWN
    ret
  _step_ball_collision_hor_right_go_hor:
    ret

  _step_ball_collision_ver:
    mov R0, [ball_dir]
    andc R0, BALL_DIR_FLIP_VER
    jz _step_ball_collision_ver_over
    xorc [ball_dir], BALL_DIR_FLIP_VER
    jmp _step_ball_collision_ver_over
