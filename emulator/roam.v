`include "emulator/lib/mux.v"
`include "emulator/ram.v"
`include "emulator/rom.v"

// MUX'ed RAM and Boot ROM.
module ROAM(out, address, read_from_ram);
    input [7:0] address;
    input read_from_ram;
    output [7:0] out;

    wire [7:0] out_ram;
    wire [7:0] out_rom;
    ROM rom(out_rom, address);
    RAM ram(out_ram, address);

    MUX_8_1 m(out, out_ram, out_rom, read_from_ram);
endmodule;
