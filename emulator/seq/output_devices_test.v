`include "emulator/seq/output_devices.v"

module OutputDevices_test;
    wire[31:0] device0_values;
    wire[31:0] device1_values;

    reg[15:0] address;
    reg is_write;
    reg clk;
    reg[31:0] value;

    OutputDevices dut(
        .device0_values(device0_values),
        .device1_values(device1_values),
        .address(address),
        .value(value),
        .is_write(is_write),
        .clk(clk));


    localparam [31:0] INPUT1 = 32'b11100101111110000100101010110001;
    localparam [31:0] INPUT2 = 32'b01011100100011000110101000000001;

    initial begin
        address = 0;
        is_write = 1;
        value = INPUT1;
        clk = 1;
        # 10
        clk = 0;
        # 10
        address = 1;
        is_write = 1;
        value = INPUT2;
        clk = 1;
        # 10
        clk = 0;
        # 10
        address = 0;
        is_write = 0;
        clk = 1;
        # 10
        clk = 0;
        $display("OUTPUT_DEVICES_TEST: address=%b is_write=%b value=%b", address, is_write, value);
        if (device0_values !== INPUT1 || device1_values !== INPUT2) begin
            $error("out failed");
            $fatal(1);
        end
    end
endmodule
