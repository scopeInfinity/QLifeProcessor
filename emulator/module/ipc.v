`define INPUT_FILE "/tmp/ourpc_input"

// Handle Inter Process Communication
// We weren't able to figure out simpler way to do so.
module IPCOut(
    input[7:0] device_id,
    input[31:0] value
    );

    always @(value) begin
        $display("IPC %x %x", device_id, value);
    end
endmodule

module IPCIn(
    output[31:0] value,
    input[7:0] device_id,
    input clk);

    // device_id to value
    reg[31:0] _ipc_input[0:7];
    always @(posedge clk) begin
        // At some random interval
        $readmemb(`INPUT_FILE, _ipc_input);
    end
    reg[31:0] _value;
    always @(*) begin
        _value <= _ipc_input[device_id];
    end
    assign value = _value;
endmodule
