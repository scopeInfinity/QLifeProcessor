`include "emulator/com/rom.v"

module rom_test;
    reg[15:0] address;
    wire[31:0] out;

    _ROM_32bit_16aline #(.filename("emulator/com/rom_test.bin"))
        dut(.out(out),
        .address(address));

    initial begin
        address = 0;
        # 10
        $display("ROM_TEST: address=%b out=%b", address, out);
        if (out !== 32'b10000010101111110111100001010111) begin
            $error("rom failed");
            $fatal(1);
        end
        address = 1*4;
        # 10
        $display("ROM_TEST: address=%b out=%b", address, out);
        if (out !== 32'b11111100101011001101000010101001) begin
            $error("rom failed");
            $fatal(1);
        end
        address = 3*4;
        # 10
        $display("ROM_TEST: address=%b out=%b", address, out);
        if (out !== 32'b11111010111111110100000111111110) begin
            $error("rom failed");
            $fatal(1);
        end
        address = 7*4;
        # 10
        $display("ROM_TEST: address=%b out=%b", address, out);
        if (out !== 32'b10011111011110101000001000101001) begin
            $error("rom failed");
            $fatal(1);
        end
    end
endmodule

module rom_boot_test;
    reg[15:0] address;
    wire[31:0] out;

    ROM_BOOT dut(.out(out),
        .address(address));

    initial begin
        address = 0;
        # 10
        $display("ROM_TEST: address=%b out=%b", address, out);
        if (out !== 32'b10000010101111110111100001010111) begin
            $error("rom failed");
            $fatal(1);
        end
    end
endmodule
