// Handle Inter Process Communication
// We were not able to figure out simpler way to do so.
module IPCOut(
    input[15:0] process_id,
    input[31:0] value
    );

    always @(value) begin
        $display("IPC %x %x", process_id, value);
    end
endmodule
