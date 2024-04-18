`include "emulator/lib/latch.v"
`include "emulator/lib/decoder.v"

module RAM_block_8bit(output[7:0] out,
           input[7:0] in,
           input is_write,
           input is_read);

    wire [7:0] lout;
    latch_d d0(.out(lout[0]), .in(in[0]), .enable(is_write));
    latch_d d1(.out(lout[1]), .in(in[1]), .enable(is_write));
    latch_d d2(.out(lout[2]), .in(in[2]), .enable(is_write));
    latch_d d3(.out(lout[3]), .in(in[3]), .enable(is_write));
    latch_d d4(.out(lout[4]), .in(in[4]), .enable(is_write));
    latch_d d5(.out(lout[5]), .in(in[5]), .enable(is_write));
    latch_d d6(.out(lout[6]), .in(in[6]), .enable(is_write));
    latch_d d7(.out(lout[7]), .in(in[7]), .enable(is_write));

    and(out[0], lout[0], is_read);
    and(out[1], lout[1], is_read);
    and(out[2], lout[2], is_read);
    and(out[3], lout[3], is_read);
    and(out[4], lout[4], is_read);
    and(out[5], lout[5], is_read);
    and(out[6], lout[6], is_read);
    and(out[7], lout[7], is_read);

endmodule;

module RAM_8bit_3aline(output[7:0] out,
           input[7:0] in,
           input[2:0] address,
           input is_write);
    // 8 byte RAM
    wire[7:0] val0, val1, val2, val3, val4, val5, val6, val7;

    wire[7:0] is_block_active;
    DECODER_8_3 decoder(.out(is_block_active), .in(address));

    RAM_block_8bit mem0(.out(val0), .in(in), .is_write(is_write & is_block_active[0]), .is_read(is_block_active[0]));
    RAM_block_8bit mem1(.out(val1), .in(in), .is_write(is_write & is_block_active[1]), .is_read(is_block_active[1]));
    RAM_block_8bit mem2(.out(val2), .in(in), .is_write(is_write & is_block_active[2]), .is_read(is_block_active[2]));
    RAM_block_8bit mem3(.out(val3), .in(in), .is_write(is_write & is_block_active[3]), .is_read(is_block_active[3]));
    RAM_block_8bit mem4(.out(val4), .in(in), .is_write(is_write & is_block_active[4]), .is_read(is_block_active[4]));
    RAM_block_8bit mem5(.out(val5), .in(in), .is_write(is_write & is_block_active[5]), .is_read(is_block_active[5]));
    RAM_block_8bit mem6(.out(val6), .in(in), .is_write(is_write & is_block_active[6]), .is_read(is_block_active[6]));
    RAM_block_8bit mem7(.out(val7), .in(in), .is_write(is_write & is_block_active[7]), .is_read(is_block_active[7]));

    assign out = val0 | val1 | val2 | val3 | val4 | val5 | val6 | val7;
endmodule;


module RAM_32bit_3aline(output[31:0] out,
           input[31:0] in,
           input[2:0] address,
           input is_write);
    // 4 * 8 byte RAM
    RAM_8bit_3aline mem0(.out(out[ 7: 0]), .in(in[ 7: 0]), .address(address), .is_write(is_write));
    RAM_8bit_3aline mem1(.out(out[15: 8]), .in(in[15: 8]), .address(address), .is_write(is_write));
    RAM_8bit_3aline mem2(.out(out[23:16]), .in(in[23:16]), .address(address), .is_write(is_write));
    RAM_8bit_3aline mem3(.out(out[31:24]), .in(in[31:24]), .address(address), .is_write(is_write));
endmodule;


module RAM_32bit_6aline(output[31:0] out,
           input[31:0] in,
           input[7:0] address,
           input is_write);
    wire[31:0] val0, val1, val2, val3, val4, val5, val6, val7;

    wire[7:0] is_block_active;
    DECODER_8_3 decoder(.out(is_block_active), .in(address[5:3]));

    RAM_32bit_3aline mem0(.out(val0), .in(in), .address(address[2:0]), .is_write(is_write & is_block_active[0]));
    RAM_32bit_3aline mem1(.out(val1), .in(in), .address(address[2:0]), .is_write(is_write & is_block_active[1]));
    RAM_32bit_3aline mem2(.out(val2), .in(in), .address(address[2:0]), .is_write(is_write & is_block_active[2]));
    RAM_32bit_3aline mem3(.out(val3), .in(in), .address(address[2:0]), .is_write(is_write & is_block_active[3]));
    RAM_32bit_3aline mem4(.out(val4), .in(in), .address(address[2:0]), .is_write(is_write & is_block_active[4]));
    RAM_32bit_3aline mem5(.out(val5), .in(in), .address(address[2:0]), .is_write(is_write & is_block_active[5]));
    RAM_32bit_3aline mem6(.out(val6), .in(in), .address(address[2:0]), .is_write(is_write & is_block_active[6]));
    RAM_32bit_3aline mem7(.out(val7), .in(in), .address(address[2:0]), .is_write(is_write & is_block_active[7]));

    wire[7:0] filter0 = {is_block_active[0],is_block_active[0],is_block_active[0],is_block_active[0],is_block_active[0],is_block_active[0],is_block_active[0],is_block_active[0]};
    wire[7:0] filter1 = {is_block_active[1],is_block_active[1],is_block_active[1],is_block_active[1],is_block_active[1],is_block_active[1],is_block_active[1],is_block_active[1]};
    wire[7:0] filter2 = {is_block_active[2],is_block_active[2],is_block_active[2],is_block_active[2],is_block_active[2],is_block_active[2],is_block_active[2],is_block_active[2]};
    wire[7:0] filter3 = {is_block_active[3],is_block_active[3],is_block_active[3],is_block_active[3],is_block_active[3],is_block_active[3],is_block_active[3],is_block_active[3]};
    wire[7:0] filter4 = {is_block_active[4],is_block_active[4],is_block_active[4],is_block_active[4],is_block_active[4],is_block_active[4],is_block_active[4],is_block_active[4]};
    wire[7:0] filter5 = {is_block_active[5],is_block_active[5],is_block_active[5],is_block_active[5],is_block_active[5],is_block_active[5],is_block_active[5],is_block_active[5]};
    wire[7:0] filter6 = {is_block_active[6],is_block_active[6],is_block_active[6],is_block_active[6],is_block_active[6],is_block_active[6],is_block_active[6],is_block_active[6]};
    wire[7:0] filter7 = {is_block_active[7],is_block_active[7],is_block_active[7],is_block_active[7],is_block_active[7],is_block_active[7],is_block_active[7],is_block_active[7]};

    assign out = (
        (val0 & {filter0,filter0,filter0,filter0}) |
        (val1 & {filter1,filter1,filter1,filter1}) |
        (val2 & {filter2,filter2,filter2,filter2}) |
        (val3 & {filter3,filter3,filter3,filter3}) |
        (val4 & {filter4,filter4,filter4,filter4}) |
        (val5 & {filter5,filter5,filter5,filter5}) |
        (val6 & {filter6,filter6,filter6,filter6}) |
        (val7 & {filter7,filter7,filter7,filter7})
    );
endmodule;
