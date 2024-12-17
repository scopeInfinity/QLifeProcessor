PROGRAM_ORG equ 48
030:  MOVC [0], 0
034:  OUT 2, [0]
038:  IN [0], 2
03c:  SHRC [0], 2
040:  MOVC [4], 4
044:  MOVC [8], 240
048:  CMPC [0], 0
04c:  JZ 108, 0
050:  OUT 2, [4]
054:  IN [12], 2
058:  STORE [[8]], [12]
05c:  ADDC [8], 4
060:  ADDC [4], 4
064:  SUBC [0], 1
068:  JMP 72, 0
06c:  JMP 240, 0
