PROGRAM_ORG equ 128
080:  MOVC [0], 0
084:  OUT 16, [0]
088:  IN [0], 0
08c:  MOVC [20], 0
090:  MOVC [4], 1
094:  MOVC [8], 64
098:  OUT 16, [4]
09c:  IN [12], 32
0a0:  STORE [[8]], [12]
0a4:  ADDC [8], 4
0a8:  ADDC [4], 4
0ac:  SUBC [0], 4
0b0:  CMP [0], [20]
0b4:  JZ 64, 0
0b8:  JMP 152, 0
