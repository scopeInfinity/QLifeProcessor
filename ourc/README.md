# Our not so C compiler

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
