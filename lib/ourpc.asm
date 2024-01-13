global _start
global MEM_IO
extern main

[SECTION .text]
_start:
    jmp main
    hlt

[SECTION .bss]
MEM_IO     resb 3
