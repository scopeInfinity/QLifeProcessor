`include "emulator/com/stage1.v"

module stage1_test;
    wire[31:0] vr_value;
    wire[7:0] input_devices_address;
    wire[15:0] ram_address;

    reg[1:0] mblock_s1;
    reg[7:0] vr_source;
    reg[31:0] input_devices_value;
    reg[31:0] ram_value;

    STAGE1 dut(
        .vr_value(vr_value),
        .input_devices_address(input_devices_address),
        .ram_address(ram_address),
        .mblock_s1(mblock_s1),
        .vr_source(vr_source),
        .input_devices_value(input_devices_value),
        .ram_value(ram_value));

    initial begin
        ram_value = 55;
        input_devices_value = 22;
        vr_source = 33;
        # 10
        mblock_s1 = 0;
        # 10
        $display("STAGE1_TEST: vr_value=%b ram_address=%b", vr_value, ram_address);
        if (vr_value !== 55 || ram_address !== 33) begin
            $error("stage1 failed");
            $fatal(1);
        end
        # 10
        mblock_s1 = 2;
        # 10
        $display("STAGE1_TEST: vr_value=%b input_devices_address=%b", vr_value, input_devices_address);
        if (vr_value !== 22 || input_devices_address !== 33) begin
            $error("stage1 failed");
            $fatal(1);
        end
        # 10
        mblock_s1 = 3;
        # 10
        $display("STAGE1_TEST: vr_value=%b const=%b", vr_value, vr_source);
        if (vr_value !== 33) begin
            $error("stage1 failed");
            $fatal(1);
        end

    end


endmodule
