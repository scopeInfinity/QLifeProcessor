#   Program
#       Two Player Ping Pong Game
#
#   Controls
#       W/S/Up/Down keyys to move bat
#   Display (16*8)
#
#   X
#   X
#   X    O          X
#                   X
#                   X
#
#

# input(1) = Keyboard({"W": 0, "S": 1, "UP": 2, "DOWN": 3})
INPUT_DEVICE equ 1

# display = LEDDisplay("LED", width_anode=16, height_cathode=8)
# output(6) = display.get_anodes()[0]
# Output(7) = display.get_cathodes()[0]
OUTPUT_WIDTH equ 6
OUTPUT_HEIGHT equ 7


PROGRAM_ORG equ 0x80

BAT_H    equ 3
BAT_MAXY equ 5

BALL_STEP_SIZE equ 3
GAME_OVER_BLINK_STEP equ 15

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

    bat1_anode_mask dd 0x7FFF
    bat2_anode_mask dd 0xFFFE
    displayoff_anode_mask dd 0xFFFF


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
    mov R0, [bat1_anode_mask]
    # cathode row
    movc R1, 0x7
    shl R1, [bat1_y]
    OUT OUTPUT_WIDTH, R0
    OUT OUTPUT_HEIGHT, R1
    movc R1, 0
    mov R0, [displayoff_anode_mask]
    OUT OUTPUT_HEIGHT, R1
    OUT OUTPUT_WIDTH, R0

    ## Player 2
    # anode col
    mov R0, [bat2_anode_mask]
    # cathode row
    movc R1, 0x7
    shl R1, [bat2_y]
    OUT OUTPUT_WIDTH, R0
    OUT OUTPUT_HEIGHT, R1
    movc R1, 0
    mov R0, [displayoff_anode_mask]
    OUT OUTPUT_HEIGHT, R1
    OUT OUTPUT_WIDTH, R0

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
    OUT OUTPUT_HEIGHT, R2
    movc R2, 0
    mov R1, [displayoff_anode_mask]
    OUT OUTPUT_HEIGHT, R2
    OUT OUTPUT_WIDTH, R1
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
