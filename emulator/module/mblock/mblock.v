`include "emulator/module/mblock/mconst.v"
`include "emulator/module/mblock/ram.v"
`include "emulator/module/mblock/rom.v"
`include "emulator/lib//mux.v"

module MBLOCK(output[31:0] out,
            input[1:0] selector,
            input[31:0] in,
            input[15:0] address,
            input is_write);

    // TODO: How can be careful about accidental write occurance
    // due to race between how the values are propogated?

    wire[31:0] out0, out1, out2, out3;

    ROM_BOOT romb(.out(out0),
        .address(address));

    RAM_32bit_16aline ram(.out(out1),
            .in(in),
            .address(address),
            .is_write(is_write & ~selector[1] & selector[0]));

    // selector 10 is reserved for IO

    MCONST mconst(.out(out3),
        .in(address));

    MUX_8_2 m0(.value(out[ 7: 0]), .A(out0[ 7: 0]), .B(out1[ 7: 0]), .D(out3[ 7: 0]), .S(selector[1:0]));
    MUX_8_2 m1(.value(out[15: 8]), .A(out0[15: 8]), .B(out1[15: 8]), .D(out3[15: 8]), .S(selector[1:0]));
    MUX_8_2 m2(.value(out[23:16]), .A(out0[23:16]), .B(out1[23:16]), .D(out3[23:16]), .S(selector[1:0]));
    MUX_8_2 m3(.value(out[31:24]), .A(out0[31:24]), .B(out1[31:24]), .D(out3[31:24]), .S(selector[1:0]));

endmodule
