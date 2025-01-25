`include "emulator/com/rom.v"
`include "emulator/module/ipc.v"
`define CONSDEV_ID 3
`define PROM_ID 2

module IODevices(
    output[31:0] value_out,
    input[7:0] device_id,
    input[31:0] value_in,
    input is_write,
    input clk);

    integer fio;

    reg[31:0] value;
    output[31:0] value_ipc_in;

    IPCOut ipcout(.device_id(device_id[7:0]), .value(value[31:0]));
    IPCIn ipcin(.value(value_ipc_in[31:0]), .device_id(device_id[7:0]), .clk(clk));

    always @(negedge clk) begin
        // Write are triggered at negedge
        if (is_write) begin
            value <= value_in;
            $display("IO:output[%x] <= %x", device_id, value_in);
        end
    end

    // PROM
    wire[31:0] prom_value;
    ROM_PINGPONG prom(.out(prom_value), .address(value_in[15:0]));

    reg[31:0] _value;
    always @(device_id) begin
        case (device_id)
            // TODO: Is it ok to use continous circuit with value_in as address?
            `PROM_ID: _value <= prom_value;
            `CONSDEV_ID: _value <= value_in;
            default:
                // Goes via IPC
                begin
                _value <= value_ipc_in;
                end
        endcase
    end
    assign value_out = _value;
endmodule
