`include "emulator/seq/io_devices.v"

module IODevices_test;
    wire[31:0] value_out;

    reg[7:0] device_id;
    reg[31:0] value_in;
    reg is_write;
    reg clk;

    IODevices dut(
        .value_out(value_out),
        .device_id(device_id),
        .value_in(value_in),
        .is_write(is_write),
        .clk(clk));

    localparam [31:0] INPUT1 = 32'b11100101111110000100101010110001;
    localparam [31:0] INPUT2 = 32'b01011100100011000110101000000001;

    initial begin
        device_id = 1;
        is_write = 1;
        value_in = INPUT1;
        clk = 1;
        # 10
        clk = 0;
        # 10
        device_id = 0;
        $display("IO_DEVICES_TEST: device_id=%b value_out=%b", device_id, value_out);
        if (value_out === INPUT1) begin
            $error("io failed");
            $fatal(1);
        end
        # 10
        device_id = 1;
        # 10
        $display("IO_DEVICES_TEST: device_id=%b value_out=%b", device_id, value_out);
        if (value_out !== INPUT1) begin
            $error("io failed");
            $fatal(1);
        end
    end
endmodule
