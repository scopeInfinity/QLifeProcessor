`include "emulator/com/stage0.v"
`include "emulator/seq/ram.v"
`include "emulator/com/rom.v"

module stage0_test;
    wire[15:0] rom_address;
    wire[31:0] rom_value;
    ROM_BOOT dut1(.out(rom_value), .address(rom_address));

    reg clk;
    reg ram_is_write;
    wire[15:0] ram_address;
    reg[31:0] ram_in;
    wire[31:0] ram_value;
    RAM_32bit_16aline dut2(
        .out(ram_value),
        .in(ram_in),
        .address(ram_address),
        .is_write(ram_is_write),
        .clk(clk));

    wire[31:0] instruction_binary;
    reg[15:0] pc;
    reg execute_from_ram;

    STAGE0 dut(
        .instruction_binary(instruction_binary),
        .ram_address(ram_address),
        .brom_address(rom_address),
        .ram_value(ram_value),
        .brom_value(rom_value),
        .pc(pc),
        .execute_from_ram(execute_from_ram));

    localparam [31:0] INPUT1 = 32'b11100101111110000100101010110001;

    initial begin
        pc = 16'b0000000000000100;
        ram_is_write = 1;
        ram_in = INPUT1;
        clk = 1;
        # 10
        clk = 0;
        # 10
        execute_from_ram = 0;
        # 10
        $display("STAGE0_TEST: pc=%b out=%b", pc, instruction_binary);
        if (instruction_binary !== 32'b11111100101011001101000010101001) begin
            $error("stage0 failed");
            $fatal(1);
        end
        # 10
        execute_from_ram = 1;
        # 10
        $display("STAGE0_TEST: pc=%b out=%b", pc, instruction_binary);
        if (instruction_binary !== INPUT1) begin
            $error("stage0 failed");
            $fatal(1);
        end

    end


endmodule
