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


BAT_H    equ 3
BAT_MAXY equ 5

section .text
  main:

  game:
    call print
    call step
    jmp game
    hlt

  wait_led_lit:
    # wait for 100 ins to let LED powered up
    mov [R0], 100
    _wait_led_lit_internal:
    sub [R0], 1
    cmp [R0], 0
    jneq _wait_led_lit_internal
    ret

  print:
    # bat1 = 7<<bat1_y
    mov [bat1_mask], 7
    shl [bat1_mask], [bat1_y]
    # bat2 = 7<<bat2_y
    mov [bat2_mask], 7
    shl [bat2_mask], [bat2_y]
    # ball_ymask = 1<<ball_y
    mov [ball_ymask], 1
    shl [ball_ymask], [ball_y]
    # ball_matrix = ball_x//8
    mov [ball_matrix], [ball_x]
    shr [ball_matrix], 3
    add [ball_matrix], 1
    # ball_xmask = 1<<(7-(ball_x%8))
    mov [R0], [ball_x]
    and [R0], 0x07
    mov [R1], 7
    sub [R1], [R0]
    mov [ball_xmask], 1
    shl [ball_xmask], [R1]

    OUT 0, [bat1_mask]
    mov [R0], 0
    OUT 1, [R0]
    call wait_led_lit
    OUT 0, [bat2_mask]
    mov [R0], 7
    OUT 2, [R0]
    call wait_led_lit
    OUT 0, [ball_ymask]
    OUT [ball_matrix], [ball_xmask]
    call wait_led_lit
    ret

  step:
    add [ball_x], 1
    and [ball_x], 0x07

section .data
    bat1_y    db 2
    bat2_y    db 2
    ball_x    db 7
    ball_y    db 3

section .bss
    bat1_mask: resb 1
    bat2_mask: resb 1
    ball_ymask: resb 1
    ball_xmask: resb 1
    ball_matrix: resb 1
