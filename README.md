[![CI](https://github.com/scopeInfinity/OurPC/actions/workflows/ci.yml/badge.svg)](https://github.com/scopeInfinity/OurPC/actions/workflows/ci.yml)

# QLife Processor
A 16-bit address, 32-bit data line general-purpose processor architecture. Key features include external ROM program execution and real-time I/O capabilities.

## Sample Programs

* Ping Pong
  * 16x8 LED display with W/S/Up/Down keyboard controller
  * Source: [ping_pong.asm](programs/ping_pong.asm)
  * Generate resolved assembly: `python3 -m planner asm -r programs/ping_pong.asm` [[example](output/programs/ping_pong_resolved.asm)]
  * Generate binary: `python3 -m planner asm -b programs/ping_pong.asm` [[example](output/programs/ping_pong.bin)]
  * Run on python emulator: `python3 -m planner compile_and_execute ping_pong`
    * ![image](https://github.com/user-attachments/assets/9fa2f68f-73ae-465c-a29c-cc92b0dc421a)
  * Run on verilog emulator: `make verilog_simulate`

## Design

### Specs

* Memory Address Line: 16-bits (points to a byte)
* Memory Value Line: 32-bits (4 bytes)
* Max Memory: 64KB
* Memory layout: [here](planner/memory.py)

#### Boot Sequence
* `programs/boot_sequence.asm` binary (aka `BROM`) is mapped from address_line `BOOTSEQUENCE_LOAD = 0x30`
* Memory Read
  * If `BOOTSEQUENCE_ORG <= address_line < DEFAULT_PROGRAM_ORG`, pulls value from `BROM`
  * Otherwise, pulls the value from `RAM`
* Execution starts with `PC` at `BOOTSEQUENCE_ORG = 0x34`
* `BROM` goal is to copy `PROM` to RAM at `DEFAULT_PROGRAM_ORG = 0x80`
* Followed by `jmp DEFAULT_PROGRAM_ORG`

#### PROM
* Programs like `programs/ping_pong.asm` are translated into binary and are referred to as `PROM`.
* `PROM` is connected to <chipset> as input-output device.
* The equivalent program is loaded in RAM at `DEFAULT_PROGRAM_ORG = 0x80`, followed by execution after boot sequence.
