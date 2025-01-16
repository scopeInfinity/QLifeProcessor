`include "emulator/com/rom.v"
`include "emulator/module/ipc.v"
`define CONSDEV_ID 3
`define PROM_ID 2

`define IO_DIR "build/emulator/io"

// Import the function called "system_init" implemented in C code

module IODevices(
    output[31:0] value_out,
    input[7:0] device_id,
    input[31:0] value_in,
    input is_write,
    input clk);

    integer fio;

    reg[31:0] _data [255:0];
    initial begin
        // $fseek(fio, 0, 0);
        // system_init();
    end
    reg[15:0] process_id;
    // assign
    reg[31:0] value;
    IPCOut ipcout(.process_id(process_id[15:0]), .value(value[31:0]));

    always @(negedge clk) begin
        // Write are triggered at negedge
        if (is_write) begin
            _data[device_id] <= value_in;
            process_id <= {8'b00000000, device_id};
            value <= value_in;


            // fio = $fopen("build/emulator/io/output.txt","w");
            // $fseek(fio, 0, 0);
            // $fwrite(fio, "%b\n", value_in);
            // $fflush(fio);
            // $fclose(fio);
            $display("IO:output[%x] <= %x", device_id, value_in);
        end
    end

    reg[31:0] _ipc_input[0:15];
    // integer i;
    always @(posedge clk) begin
        // At some random interval
        $readmemb("/tmp/ourpc_input.txt", _ipc_input);
        // for (i=0; i<16; i=i+1) begin
        //     $display("INPUT[%d]: %x", i, _ipc_input[i]);
        // end
    end

    // PROM
    wire[31:0] prom_value;
    ROM_PINGPONG prom(.out(prom_value), .address(_data[`PROM_ID][15:0]));

    reg[31:0] _value;
    always @(device_id) begin
        case (device_id)
            `PROM_ID: _value <= prom_value;
            default:
                begin
                _value <= _ipc_input[device_id];
                // $display("IO:input[%x] <= %x", device_id, _value);
                end
        endcase
    end
    assign value_out = _value;
endmodule
