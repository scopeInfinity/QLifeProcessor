module InputDevices(
    output[31:0] value,
    input[7:0] address,
    input[31:0] device0_values,
    input[31:0] device1_values);

    reg[31:0] _value;
    always @(address) begin
        case (address)
            0: _value = device0_values;
            1: _value = device1_values;
        endcase
    end
    assign value = _value;
endmodule
