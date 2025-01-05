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
        if (out !== 32'b01010111011110001011111110000010) begin
            $error("rom failed");
            $fatal(1);
        end
        address = 3*4;
        # 10
        $display("ROM_TEST: address=%b out=%b", address, out);
        if (out !== 32'b11111110010000011111111111111010) begin
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
        address = 'h40;
        # 10
        $display("BROM_TEST: address=%b out=%b", address, out);
        if (out !== 32'b00000000000000000000000001000100) begin
            $error("rom failed");
            $fatal(1);
        end
    end
endmodule
