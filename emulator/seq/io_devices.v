`include "emulator/com/rom.v"
`define CONSDEV_ID 1
`define PROM_ID 2

module IODevices(
    output[31:0] value_out,
    input[7:0] device_id,
    input[31:0] value_in,
    input is_write,
    input clk);

    reg[31:0] _data [255:0];
    always @(negedge clk) begin
        // Write are triggered at negedge
        if (is_write) begin
            _data[device_id] <= value_in;
            $display("IO:output[%x] <= %x", device_id, value_in);
        end
    end

    // PROM
    wire[31:0] prom_value;
    ROM_PINGPONG prom(.out(prom_value), .address(_data[`PROM_ID][15:0]));

    reg[31:0] _value;
    always @(device_id) begin
        case (device_id)
            `PROM_ID: _value <= prom_value;
            `CONSDEV_ID: _value <= _data[`CONSDEV_ID];
        endcase
    end
    assign value_out = _value;
endmodule
