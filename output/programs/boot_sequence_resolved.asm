PROGRAM_ORG equ 52
034:  MOVC [0], 0
038:  OUT 2, [0]
03c:  IN [0], 2
040:  SHRC [0], 2
044:  MOVC [4], 4
048:  MOVC [8], 128
04c:  CMPC [0], 0
050:  JZ 112, 0
054:  OUT 2, [4]
058:  IN [12], 2
05c:  STORE [[8]], [12]
060:  ADDC [8], 4
064:  ADDC [4], 4
068:  SUBC [0], 1
06c:  JMP 76, 0
070:  JMP 128, 0
