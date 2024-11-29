module RAM_32bit_16aline(output[31:0] out,
           input[31:0] in,
           input[15:0] address,
           input is_write);
    // 4 * 64KB RAM

    reg[31:0] mem [65535:0];
    always @(address, in, is_write) begin
        if (is_write) begin
        mem[address] <= in;
        end
    end
    assign out = mem[address];

endmodule
