`include "emulator/seq/ram.v"

module RAM_32bit_16aline_test;
    reg[15:0] address;
    reg is_write;
    reg clk;
    reg[31:0] in;
    wire[31:0] out;

    localparam [31:0] INPUT1 = 32'b11100101111110000100101010110001;
    localparam [31:0] INPUT2 = 32'b01011100100011000110101000000001;

    RAM_32bit_16aline dut(.out(out),
           .in(in),
           .address(address),
           .is_write(is_write),
           .clk(clk));

    initial begin
        address = 16'b1100001110111100;
        is_write = 1;
        in = INPUT1;
        clk = 1;
        # 10
        clk = 0;
        # 10
        $display("RAM_TEST: address=%b is_write=%b in=%b out=%b", address, is_write, in, out);
        if (out !== INPUT1) begin
            $error("ram failed");
            $fatal(1);
        end

        address = 16'b1100001110111100;
        is_write = 0;
        # 10
        in = INPUT2;
        # 10
        clk = 1;
        # 10
        clk = 0;
        $display("RAM_TEST: address=%b is_write=%b in=%b out=%b", address, is_write, in, out);
        if (out !== INPUT1) begin
            $error("ram failed");
            $fatal(1);
        end

        address = 16'b1011100000111010;
        in = INPUT2;
        # 10
        is_write = 1;
        # 10
        clk = 1;
        # 10
        clk = 0;
        # 10
        $display("RAM_TEST: address=%b is_write=%b in=%b out=%b", address, is_write, in, out);
        if (out !== INPUT2) begin
            $error("ram failed");
            $fatal(1);
        end

        is_write = 0;
        address = 16'b1100001110111100;
        # 10
        $display("RAM_TEST: address=%b is_write=%b in=%b out=%b", address, is_write, in, out);
        if (out !== INPUT1) begin
            $error("ram failed");
            $fatal(1);
        end

        address = 16'b1011100000111010;
        # 10
        $display("RAM_TEST: address=%b is_write=%b in=%b out=%b", address, is_write, in, out);
        if (out !== INPUT2) begin
            $error("ram failed");
            $fatal(1);
        end

    end
endmodule
