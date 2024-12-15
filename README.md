[![CI](https://github.com/scopeInfinity/OurPC/actions/workflows/ci.yml/badge.svg)](https://github.com/scopeInfinity/OurPC/actions/workflows/ci.yml)

# OurPC
(picking a name is hard and is deferred for later)

The eventual goal(?) is to build a general-purpose processor integrated with simple input (e.g. buttons) and output devices (8x8 LED display).

## Sample Programs

* Ping Pong
  * Source: [ping_pong.asm](programs/ping_pong.asm)
  * Generate resolved assembly: `python3 -m planner asm -r programs/ping_pong.asm` [[example](output/programs/ping_pong_resolved.asm)]
  * Generate binary: `python3 -m planner asm -b programs/ping_pong.asm` [[example](output/programs/ping_pong.bin)]
  * Run on emulator: `python3 -m planner compile_and_execute ping_pong`

## Design

This section is not up-to date.

### Specs

* Address Line: 16-bits
* Max Memory: 64KB

### Constants

* INSZ = 0x20, independent input bytes
* OUTSZ = 0x20, independent output bytes
* IPC = 0x0100, intial value of `PC` (or Program Counter).

### Memory Allocation

* `RAM[0:INSZ]` is mapped to I/O module input
* `RAM[INSZ:OUTSZ]` is mapped to I/O module output
* `RAM[IPC:IPC+x]` is loaded from ROM. So it essentially contains `.text`, `.data`.

### Sequencing


* At boot
  * Load `ROM[0:x]` into `RAM[IPC:IPC+x]`
    * TODO: How?

### Assembly

* `.bss` must be the last section.
* Registers don't really exists. `R[0-7]` are mapped to memory location in `.bss` for convenience and some instructions return response.

### Architecture

#### I/O

Hardware interact asynchronously with IOM (I/O Module) which then interact with RAM at program's will. (WE ARE NOT DOING IT)

* Input devices publish state change in IOM and Output devices read from IOM.
* Program use `IN <index>` instructions to read from `IOM_in[index]` and write to `RAM[index]`. `IOM_in` won't cache input and it will be read as real-time value. If a input state needs to be cached, it's the input device responsibility.
* Program use `OUT <index>` instructions to read `RAM[INSZ+index]` and write to `IOM_out[index]`.



# TODO

## Processor

* Address bits: 8
* Register size: 8
* Memory size: 2**8 = 256 bytes

### Idea

To keep number of component small, we would split a single instruction execution period into 4 cycles.

* Reset
  * Set `PC = 0`
  * sub-cycle clock to cycle-0
* Cycle 0
  * Fetch instruction from `ROM[$PC]` into `pin_INS`
* Cycle 1
  * Perform first read

## Assembler

### Details

* Registers: R0, R1, R2, R3 or `R{NUM}`

* Input/Output pin: IO0, IO1, ..., IO7 or `IO{NUM}` (8-bits)

### Instructions

* `IN R{NUM}`: short-blocking input with 8-bit response.
* `OUT R{NUM}`: short-blocking 8-bit output.

## Syntax: High Level

Not yet defined.
