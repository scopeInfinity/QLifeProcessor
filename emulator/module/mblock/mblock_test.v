`include "emulator/module/mblock/mblock.v"

module BLOCK_32bit_16aline_test;
    wire[31:0] out;
    reg[15:0] address;
    reg[1:0] selector;
    reg[31:0] in;
    reg is_write;

    localparam [31:0] INPUT16z = 16'bzzzzzzzzzzzzzzzz;
    localparam [31:0] INPUT32z = 32'bzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz;
    localparam [31:0] INPUT1 = 32'b11100101111110000100101010110001;
    localparam [31:0] INPUT2 = 32'b01011100100011000110101000000001;

    MBLOCK dut(.out(out),
           .selector(selector),
           .in(in),
           .address(address),
           .is_write(is_write));

    initial begin
        selector = 2'b01;  // RAM write
        address = 16'b1011100000111010;
        in = INPUT1;
        # 10
        is_write = 1;
        # 10
        $display("MBLOCK: RAM_TEST: address=%b is_write=%b in=%b out=%b", address, is_write, in, out);
        if (out !== INPUT1) begin
            $error("mblock failed");
            $fatal(1);
        end

        selector = 2'b00;  // ROM_BOOT
        address = 16'b0000000000000001;
        is_write = 1'bz;
        in = INPUT32z;
        # 10
        $display("MBLOCK: ROM_TEST: address=%b is_write=%b in=%b out=%b", address, is_write, in, out);
        if (out !== 32'b11111100101011001101000010101001) begin
            $error("mblock failed");
            $fatal(1);
        end

        selector = 2'b11;  // MCONST
        address = 16'b0001100100111101;
        is_write = 1'bz;
        in = INPUT32z;
        # 10
        $display("MBLOCK: MCONST: address=%b is_write=%b in=%b out=%b", address, is_write, in, out);
        if (out !== 32'b00000000000000000001100100111101) begin
            $error("mblock failed");
            $fatal(1);
        end

        selector = 2'b01;  // RAM read
        address = 16'b1011100000111010;
        is_write = 0;
        # 10
        in = INPUT32z;
        # 10
        $display("MBLOCK: RAM_TEST: address=%b is_write=%b in=%b out=%b", address, is_write, in, out);
        if (out !== INPUT1) begin
            $error("mblock failed");
            $fatal(1);
        end
    end
endmodule
