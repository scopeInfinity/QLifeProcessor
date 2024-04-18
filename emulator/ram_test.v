`include "emulator/ram.v"

module ram_block_test;
    reg is_read;
    reg is_write;
    reg[7:0] in;
    wire[7:0] out;

    localparam [7:0] INPUT1 = 8'b01100101;
    localparam [7:0] INPUT2 = 8'b10111011;

    RAM_block_8bit dut(.out(out),
           .in(in),
           .is_write(is_write),
           .is_read(is_read));

    initial begin
        in = INPUT1;
        is_write = 1;
        is_read = 1;
        # 10
        $display("RAM_BLOCK_TEST: is_read=%b is_write=%b in=%b out=%b", is_read, is_write, in, out);
        if (out !== INPUT1) begin
            $error("ram_block failed");
            $fatal(1);
        end

        is_write = 0;
        is_read = 1;
        # 10
        $display("RAM_BLOCK_TEST: is_read=%b is_write=%b in=%b out=%b", is_read, is_write, in, out);
        if (out !== INPUT1) begin
            $error("ram_block failed");
            $fatal(1);
        end

        is_write = 0;
        is_read = 0;
        # 10
        $display("RAM_BLOCK_TEST: is_read=%b is_write=%b in=%b out=%b", is_read, is_write, in, out);
        if (out !== 0) begin
            $error("ram_block failed");
            $fatal(1);
        end

        in = INPUT2;
        is_write = 1;
        is_read = 0;
        # 10
        $display("RAM_BLOCK_TEST: is_read=%b is_write=%b in=%b out=%b", is_read, is_write, in, out);
        if (out !== 0) begin
            $error("ram_block failed");
            $fatal(1);
        end

        is_write = 0;
        is_read = 1;
        # 10
        $display("RAM_BLOCK_TEST: is_read=%b is_write=%b in=%b out=%b", is_read, is_write, in, out);
        if (out !== INPUT2) begin
            $error("ram_block failed");
            $fatal(1);
        end

        in = INPUT1;
        is_write = 0;
        is_read = 1;
        # 10
        $display("RAM_BLOCK_TEST: is_read=%b is_write=%b in=%b out=%b", is_read, is_write, in, out);
        if (out !== INPUT2) begin
            $error("ram_block failed");
            $fatal(1);
        end

        is_read = 0;
        # 10
        $display("RAM_BLOCK_TEST: is_read=%b is_write=%b in=%b out=%b", is_read, is_write, in, out);
        if (out !== 0) begin
            $error("ram_block failed");
            $fatal(1);
        end

    end
endmodule

module ram_8bit_3aline_test;
    reg[2:0] address;
    reg is_write;
    reg[7:0] in;
    wire[7:0] out;

    localparam [7:0] INPUT1 = 8'b01100101;
    localparam [7:0] INPUT2 = 8'b10111011;

    RAM_8bit_3aline dut(.out(out),
           .in(in),
           .address(address),
           .is_write(is_write));

    initial begin
        address = 0;
        is_write = 1;
        in = INPUT1;
        # 10
        $display("RAM_TEST: address=%b is_write=%b in=%b out=%b", address, is_write, in, out);
        if (out !== INPUT1) begin
            $error("ram failed");
            $fatal(1);
        end

        address = 0;
        is_write = 0;
        # 10
        in = INPUT2;
        # 10
        $display("RAM_TEST: address=%b is_write=%b in=%b out=%b", address, is_write, in, out);
        if (out !== INPUT1) begin
            $error("ram failed");
            $fatal(1);
        end

        address = 1;
        in = INPUT2;
        # 10
        is_write = 1;
        # 10
        $display("RAM_TEST: address=%b is_write=%b in=%b out=%b", address, is_write, in, out);
        if (out !== INPUT2) begin
            $error("ram failed");
            $fatal(1);
        end

        is_write = 0;
        # 10
        address = 0;
        # 10
        $display("RAM_TEST: address=%b is_write=%b in=%b out=%b", address, is_write, in, out);
        if (out !== INPUT1) begin
            $error("ram failed");
            $fatal(1);
        end

        address = 1;
        # 10
        $display("RAM_TEST: address=%b is_write=%b in=%b out=%b", address, is_write, in, out);
        if (out !== INPUT2) begin
            $error("ram failed");
            $fatal(1);
        end

    end
endmodule


module ram_32bit_3aline_test;
    reg[2:0] address;
    reg is_write;
    reg[31:0] in;
    wire[31:0] out;

    localparam [7:0] INPUT1 = 32'b11100101111110000100101010110001;
    localparam [7:0] INPUT2 = 32'b01011100100011000110101000000001;

    RAM_32bit_3aline dut(.out(out),
           .in(in),
           .address(address),
           .is_write(is_write));

    initial begin
        address = 0;
        is_write = 1;
        in = INPUT1;
        # 10
        $display("RAM_TEST: address=%b is_write=%b in=%b out=%b", address, is_write, in, out);
        if (out !== INPUT1) begin
            $error("ram failed");
            $fatal(1);
        end

        address = 0;
        is_write = 0;
        # 10
        in = INPUT2;
        # 10
        $display("RAM_TEST: address=%b is_write=%b in=%b out=%b", address, is_write, in, out);
        if (out !== INPUT1) begin
            $error("ram failed");
            $fatal(1);
        end

        address = 1;
        in = INPUT2;
        # 10
        is_write = 1;
        # 10
        $display("RAM_TEST: address=%b is_write=%b in=%b out=%b", address, is_write, in, out);
        if (out !== INPUT2) begin
            $error("ram failed");
            $fatal(1);
        end

        is_write = 0;
        # 10
        address = 0;
        # 10
        $display("RAM_TEST: address=%b is_write=%b in=%b out=%b", address, is_write, in, out);
        if (out !== INPUT1) begin
            $error("ram failed");
            $fatal(1);
        end

        address = 1;
        # 10
        $display("RAM_TEST: address=%b is_write=%b in=%b out=%b", address, is_write, in, out);
        if (out !== INPUT2) begin
            $error("ram failed");
            $fatal(1);
        end

    end
endmodule


module ram_32bit_6aline_test;
    reg[7:0] address;
    reg is_write;
    reg[31:0] in;
    wire[31:0] out;

    localparam [7:0] INPUT1 = 32'b11100101111110000100101010110001;
    localparam [7:0] INPUT2 = 32'b01011100100011000110101000000001;

    RAM_32bit_6aline dut(.out(out),
           .in(in),
           .address(address),
           .is_write(is_write));

    initial begin
        address = 43;
        is_write = 1;
        in = INPUT1;
        # 10
        $display("RAM_TEST: address=%b is_write=%b in=%b out=%b", address, is_write, in, out);
        if (out !== INPUT1) begin
            $error("ram failed");
            $fatal(1);
        end

        address = 43;
        is_write = 0;
        # 10
        in = INPUT2;
        # 10
        $display("RAM_TEST: address=%b is_write=%b in=%b out=%b", address, is_write, in, out);
        if (out !== INPUT1) begin
            $error("ram failed");
            $fatal(1);
        end

        address = 28;
        in = INPUT2;
        # 10
        is_write = 1;
        # 10
        $display("RAM_TEST: address=%b is_write=%b in=%b out=%b", address, is_write, in, out);
        if (out !== INPUT2) begin
            $error("ram failed");
            $fatal(1);
        end

        is_write = 0;
        # 10
        address = 43;
        # 10
        $display("RAM_TEST: address=%b is_write=%b in=%b out=%b", address, is_write, in, out);
        if (out !== INPUT1) begin
            $error("ram failed");
            $fatal(1);
        end

        address = 28;
        # 10
        $display("RAM_TEST: address=%b is_write=%b in=%b out=%b", address, is_write, in, out);
        if (out !== INPUT2) begin
            $error("ram failed");
            $fatal(1);
        end

    end
endmodule
