module RAM_32bit_16aline(
    output[31:0] out,
    input[31:0] in,
    input[15:0] address,
    input is_write,
    input clk);
    // 64KB RAM

    reg[31:0] mem [65535:0];
    always @(negedge clk) begin
        // Write are triggered at negedge
        if (is_write) begin
            mem[address] <= in;
            $display("RAM[%x] <= %x", address, in);
        end
    end
    assign out = mem[address];

endmodule
