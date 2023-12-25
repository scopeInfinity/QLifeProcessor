;extern main
;extern init_sim
global MEM_IO

[SECTION .text]
;a_start:
;        call init_sim
;        call main

[SECTION .bss]
MEM_IO     resb 3
