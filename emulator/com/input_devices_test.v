`include "emulator/com/input_devices.v"

module InputDevices_test;
    localparam [31:0] INPUT1 = 32'b11100101111110000100101010110001;
    localparam [31:0] INPUT2 = 32'b01011100100011000110101000000001;

    reg[31:0] device0_values = INPUT1;
    reg[31:0] device1_values = INPUT2;
    reg[7:0] address;

    wire[31:0] value;

    InputDevices dut(
        .value(value),
        .address(address),
        .device0_values(device0_values),
        .device1_values(device1_values));

    initial begin
        address = 0;
        # 10
        $display("INPUT_DEVICES_TEST: address=%b value=%b", address, value);
        if (value !== INPUT1) begin
            $error("in failed");
            $fatal(1);
        end
        address = 1;
        # 10
        $display("INPUT_DEVICES_TEST: address=%b value=%b", address, value);
        if (value !== INPUT2) begin
            $error("in failed");
            $fatal(1);
        end
    end
endmodule
