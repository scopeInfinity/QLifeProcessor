module OutputDevices(
    output[31:0] device0_values,
    output[31:0] device1_values,
    input[15:0] address,
    input[31:0] value,
    input is_write,
    input clk);

    reg[31:0] _data [65535:0];
    always @(negedge clk) begin
        // Write are triggered at negedge
        if (is_write) begin
        _data[address] <= value;
        end
    end
    assign device0_values = _data[0];
    assign device1_values = _data[1];
endmodule
