`include "emulator/com/stage2.v"

module stage2_test;
    wire[31:0] vrw_value;
    wire[31:0] vw_value;
    wire[15:0] ram_address;
    wire alu_is_zero;

    reg[2:0] mblock_s2;
    reg[7:0] vr_source;
    reg[31:0] vr_value;
    reg[7:0] vrw_source;
    reg[3:0] alu_op;
    reg[15:0] pc;
    reg[31:0] ram_value;

    STAGE2 dut(
        .vrw_value(vrw_value),
        .vw_value(vw_value),
        .ram_address(ram_address),
        .alu_is_zero(alu_is_zero),
        .mblock_s2(mblock_s2),
        .vr_source(vr_source),
        .vr_value(vr_value),
        .vrw_source(vrw_source),
        .alu_op(alu_op),
        .pc(pc),
        .ram_value(ram_value));

    initial begin
        vr_source = 10;
        vr_value = 1000;
        vrw_source = 20;
        alu_op = 0; // add
        pc = 84;
        ram_value = 99;
        # 10
        mblock_s2 = 0;
        # 10
        $display("STAGE2_TEST: vrw_value=%b vw_value=%b alu_is_zero=%b ram_address=%b", vrw_value, vw_value, alu_is_zero, ram_address);
        if (vrw_value !== 99 || ram_address !== 20 || vw_value != 1099 || alu_is_zero != 0) begin
            $error("stage2 failed");
            $fatal(1);
        end
        # 10
        mblock_s2 = 1;
        # 10
        $display("STAGE2_TEST: vrw_value=%b vw_value=%b alu_is_zero=%b ram_address=%b", vrw_value, vw_value, alu_is_zero, ram_address);
        if (vrw_value !== 99 || ram_address !== 1000 || vw_value != 1099 || alu_is_zero != 0) begin
            $error("stage2 failed");
            $fatal(1);
        end
        # 10
        mblock_s2 = 2;
        # 10
        $display("STAGE2_TEST: vrw_value=%b vw_value=%b alu_is_zero=%b ram_address=%b", vrw_value, vw_value, alu_is_zero, ram_address);
        if (vrw_value !== 99 || ram_address !== ((10<<8)|20) || vw_value != 1099 || alu_is_zero != 0) begin
            $error("stage2 failed");
            $fatal(1);
        end
        # 10
        mblock_s2 = 4;
        # 10
        $display("STAGE2_TEST: vrw_value=%b vw_value=%b alu_is_zero=%b", vrw_value, vw_value, alu_is_zero);
        if (vrw_value !== 20 || vw_value != 1020 || alu_is_zero != 0) begin
            $error("stage2 failed");
            $fatal(1);
        end
        # 10
        mblock_s2 = 6;
        # 10
        $display("STAGE2_TEST: vrw_value=%b vw_value=%b alu_is_zero=%b ram_address=%b", vrw_value, vw_value, alu_is_zero, ram_address);
        if (vrw_value !== ((10<<8)|20)  || vw_value !=  (((10<<8)|20)+1000) || alu_is_zero != 0) begin
            $error("stage2 failed");
            $fatal(1);
        end
        # 10
        mblock_s2 = 7;
        # 10
        $display("STAGE2_TEST: vrw_value=%b vw_value=%b alu_is_zero=%b ram_address=%b", vrw_value, vw_value, alu_is_zero, ram_address);
        if (vrw_value !== 84 || vw_value != 1084 || alu_is_zero != 0) begin
            $error("stage2 failed");
            $fatal(1);
        end
        # 10
        mblock_s2 = 0;
        alu_op = 1; // sub
        ram_value = 1000;
        # 10
        $display("STAGE2_TEST: vrw_value=%b vw_value=%b alu_is_zero=%b ram_address=%b", vrw_value, vw_value, alu_is_zero, ram_address);
        if (vrw_value !== 1000 || ram_address !== 20 || vw_value != 0 || alu_is_zero != 1) begin
            $error("stage2 failed");
            $fatal(1);
        end
    end


endmodule
