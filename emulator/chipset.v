`include "emulator/module/clock.v"
`include "emulator/seq/register.v"


module CHIPSET(
    input reset,
    input[31:0] ram_value,
    output[31:0] ram_address,
    output ram_is_write,
    );

    reg is_powered_on;
    reg execute_from_ram;
    reg[15:0] pc, pc_next;

    // Clock
    wire[0:3] clk;
    CLOCK clock(
        .clk(clk[0:3]));

    // BROM
    wire[15:0] brom_address;
    wire[31:0] brom_value;
    ROM_BOOT brom(.out(brom_value), .address(brom_address));

    // RAM
    reg ram_is_write;
    wire[15:0] ram_address;
    reg[31:0] ram_in;
    wire[31:0] ram_value;
    RAM_32bit_16aline ram(
        .out(ram_value),
        .in(ram_in),
        .address(ram_address),
        .is_write(ram_is_write),
        .clk(clk[3]));


    wire[15:0] ram_address_stage0;
    // TODO: Updated ram_address
    assign ram_address = ram_address_stage0;



    // Boot Sequence
    //
    // When the device have power supply but `is_powered_on` is off. The pc_eval
    // forces `program_counter_next` to be 0 and `execute_from_brom` to True.
    // If we keep the `is_powered_on` button in off stage for at-least 4 cycles
    // then at "stage3 posedge" program_counter should get updated to 0.
    // After that for every "stage0 posedge" till is_powered_on is off,
    // program_counter:0 along with execute_from_brom:True will be used to pull
    // up and execute first instruction from BROM.
    //
    // Assumption: No stateful IO devices are connected.
    // TODO: Implement `execute_from_brom` update implementation.

    // Operates on clk[3] down
    BOOT_CONTROL boot_control(
        .is_powered_on(is_powered_on),
        .pc_next(pc_next),
        .flags(flags),
        .reset(reset),
        .clk(clk[3]),
        );


    // Following circuit is continous within each stages
    // with exception of RAM write which relies on clock;
    // wire[15:0] program_counter;
    // wire[1:0] mblock_selector;
    // wire[15:0] mblock_address;
    // wire[31:0] mblock_input;
    // wire[31:0] mblock_output;
    // wire mblock_write;


    // STAGE0
    wire[31:0] instruction_binary;
    STAGE0 instruction_resolver(
        .instruction_binary(instruction_binary),
        .ram_address(ram_address_stage0),
        .brom_address(brom_address),
        .ram_value(ram_value),
        .brom_value(brom_value),
        .pc(pc),
        .execute_from_ram(execute_from_ram));

    // STAGE1
    wire[31:0] instruction_binary_cached;
    REGISTER_up_16b r_ins_bin(
        .out(instruction_binary_cached),
        .in(instruction_binary),
        .clk(clk[1]));

    wire[3:0] mblock_alu_op = instruction_binary_cached[3:0];
    wire[3:0] mblock_s1 = instruction_binary_cached[5:4];
    wire[1:0] mblock_s2 = instruction_binary_cached[8:6];
    wire[2:0] mblock_s3 = instruction_binary_cached[11:9];
    wire[7:0] vrw_source = instruction_binary_cached[23:16];
    wire[7:0] vr_source = instruction_binary_cached[31:24];



    // STAGE1

    // TODO: Breakdown instruction_op into sub-operations

    // TODO: Ensure MBLOCK supplies expectations.
    // MBLOCK_MUX is expected to fetch MBLOCK based on v0_source and
    // instruction_op breakdowns and redirect the value into v0.

    // @stage1 posedge following should freeze.
    wire[31:0] vr_value;
;
    FETCH_AND_STORE stage1(
        .vr_value(vr_value),
        .is_powered_on(is_powered_on),
        .pc_next(pc_next),
        .pc(pc),
        .vr_source(vr_source),
        .mblock_s1(mblock_s1),
        .clk(clk[1]));

    // STAGE2

    // TODO: Ensure MBLOCK supplies expectations.
    // MBLOCK_MUX is expected to fetch MBLOCK based on v0_source and
    // instruction_op breakdowns and redirect the value into v0.

    // @stage2 posedge following should freeze.
    wire[31:0] vrw_value;
    FETCH_AND_STORE stage2(
        .vrw_value(vrw_value),
        .is_powered_on(is_powered_on),
        .vr_source(vr_source),
        .vr_value(vr_value),
        .vrw_source(vr_source),
        .mblock_s2(mblock_s2),
        .clk(clk2));

    wire[31:0] vw_value;
    ALU alu(
        .out(vw_value),
        .is_zero(flags[FLAGS_BIT_VW_ZERO]),
        .vr_value(vr_value),
        .vrw_value(vrw_value),
        .op(mblock_alu_op));

    // @stage3 posedge following should freeze.
    FETCH_AND_STORE stage2(
        .vw_value(vw_value),
        .vrw_value(vrw_value),
        .vrw_source(vrw_source),
        .mblock_s3(mblock_s3),
        .clk(clk3));

endmodule