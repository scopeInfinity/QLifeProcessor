`include "emulator/com/stage3.v"

module stage3_test;
    wire[31:0] output_devices_value;
    wire[7:0] output_devices_address;
    wire[15:0] ram_address;
    wire[31:0] ram_in;
    wire ram_is_write;
    wire output_is_write;
    wire[15:0] pc_next;
    wire execute_from_ram_new;
    wire is_powered_on_new;

    reg[2:0] mblock_s3;
    reg[31:0] vrw_value;
    reg[31:0] vw_value;
    reg[7:0] vrw_source;
    reg[15:0] pc;
    reg is_powered_on;
    reg flag_last_zero;
    reg execute_from_ram;
    reg reset_button;

    STAGE3 dut(
    .output_devices_value(output_devices_value),
    .output_devices_address(output_devices_address),
    .ram_address(ram_address),
    .ram_in(ram_in),
    .ram_is_write(ram_is_write),
    .output_is_write(output_is_write),
    .pc_next(pc_next),
    .execute_from_ram_new(execute_from_ram_new),
    .is_powered_on_new(is_powered_on_new),
    .mblock_s3(mblock_s3),
    .vrw_value(vrw_value),
    .vw_value(vw_value),
    .vrw_source(vrw_source),
    .pc(pc),
    .is_powered_on(is_powered_on),
    .flag_last_zero(flag_last_zero),
    .execute_from_ram(execute_from_ram),
    .reset_button(reset_button));

    initial begin
        reset_button = 0;
        is_powered_on = 1;
        execute_from_ram = 1;
        pc = 10;
        flag_last_zero = 0;
        mblock_s3 = 0;
        # 10
        $display("STAGE3_TEST: mblock_s3=%b pc_next=%b write_ram=%b write_out=%b radd=%b rin=%b", mblock_s3, pc_next, ram_is_write, output_is_write, ram_address, ram_in);
        if (pc_next!==14 || ram_is_write!==0 || output_is_write!==0) begin
            $error("stage3 failed");
            $fatal(1);
        end

        mblock_s3 = 1;
        vw_value = 99;
        vrw_source = 15;
        # 10
        $display("STAGE3_TEST: mblock_s3=%b pc_next=%b write_ram=%b write_out=%b radd=%b rin=%b", mblock_s3, pc_next, ram_is_write, output_is_write, ram_address, ram_in);
        if (pc_next!==14 || ram_address!==15 || ram_in!==99 || ram_is_write!==1 || output_is_write!==0) begin
            $error("stage3 failed");
            $fatal(1);
        end

        mblock_s3 = 2;
        vw_value = 99;
        vrw_source = 15;
        # 10
        $display("STAGE3_TEST: mblock_s3=%b pc_next=%b write_ram=%b write_out=%b radd=%b rin=%b", mblock_s3, pc_next, ram_is_write, output_is_write, ram_address, ram_in);
        if (pc_next!==14 || output_devices_address!==15 || output_devices_value!==99 || ram_is_write!==0 || output_is_write!==1) begin
            $error("stage3 failed");
            $fatal(1);
        end

        mblock_s3 = 3;
        vw_value = 99;
        vrw_value = 97;
        vrw_source = 15;
        # 10
        $display("STAGE3_TEST: mblock_s3=%b pc_next=%b write_ram=%b write_out=%b radd=%b rin=%b", mblock_s3, pc_next, ram_is_write, output_is_write, ram_address, ram_in);
        if (pc_next!==14 || ram_address!==97 || ram_in!==99 || ram_is_write!==1 || output_is_write!==0) begin
            $error("stage3 failed");
            $fatal(1);
        end

        mblock_s3 = 4;
        vw_value = 99;
        flag_last_zero = 0;
        # 10
        $display("STAGE3_TEST: mblock_s3=%b pc_next=%b write_ram=%b write_out=%b", mblock_s3, pc_next, ram_is_write, output_is_write);
        if (pc_next!==99 || ram_is_write!==0 || output_is_write!==0) begin
            $error("stage3 failed");
            $fatal(1);
        end

        mblock_s3 = 5;
        flag_last_zero = 1;
        # 10
        $display("STAGE3_TEST: mblock_s3=%b pc_next=%b write_ram=%b write_out=%b", mblock_s3, pc_next, ram_is_write, output_is_write);
        if (pc_next!==99 || ram_is_write!==0 || output_is_write!==0) begin
            $error("stage3 failed");
            $fatal(1);
        end
        flag_last_zero = 0;
        # 10
        $display("STAGE3_TEST: mblock_s3=%b pc_next=%b write_ram=%b write_out=%b", mblock_s3, pc_next, ram_is_write, output_is_write);
        if (pc_next!==14 || ram_is_write!==0 || output_is_write!==0) begin
            $error("stage3 failed");
            $fatal(1);
        end

        mblock_s3 = 6;
        flag_last_zero = 0;
        # 10
        $display("STAGE3_TEST: mblock_s3=%b pc_next=%b write_ram=%b write_out=%b", mblock_s3, pc_next, ram_is_write, output_is_write);
        if (pc_next!==99 || ram_is_write!==0 || output_is_write!==0) begin
            $error("stage3 failed");
            $fatal(1);
        end
        flag_last_zero = 1;
        # 10
        $display("STAGE3_TEST: mblock_s3=%b pc_next=%b write_ram=%b write_out=%b", mblock_s3, pc_next, ram_is_write, output_is_write);
        if (pc_next!==14 || ram_is_write!==0 || output_is_write!==0) begin
            $error("stage3 failed");
            $fatal(1);
        end

        mblock_s3 = 7;
        # 10
        $display("STAGE3_TEST: mblock_s3=%b", mblock_s3);
        if (is_powered_on_new !== 0 || execute_from_ram_new !== 1) begin
            $error("stage3 failed");
            $fatal(1);
        end

        mblock_s3 = 0;
        reset_button = 1;
        is_powered_on = 0;
        # 10
        $display("STAGE3_TEST: mblock_s3=%b pc_next=%b", mblock_s3, pc_next);
        if (pc_next !== 'h44 || is_powered_on_new !== 1 || execute_from_ram_new !== 0) begin
            $error("stage3 failed");
            $fatal(1);
        end
    end
endmodule
