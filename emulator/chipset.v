`include "emulator/module/clock.v"
`include "emulator/seq/register.v"
`include "emulator/com/stage0.v"
`include "emulator/com/stage1.v"


module CHIPSET(
    input reset,
    input[31:0] ram_value,
    output[31:0] ram_address,
    output ram_is_write,
    );

    reg is_powered_on;
    reg flag_execute_from_ram;
    reg flag_last_zero;
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
    wire[15:0] ram_address_stage1;
    // TODO: Updated ram_address
    assign ram_address = ram_address_stage0;

    // Input Devices
    wire[7:0] input_devices_address;
    reg[31:0] input_devices_value;
    // TODO: add devices modules

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

    // STAGE0
    wire[31:0] _instruction_binary;
    STAGE0 stage0(
        .instruction_binary(_instruction_binary),
        .ram_address(ram_address_stage0),
        .brom_address(brom_address),
        .ram_value(ram_value),
        .brom_value(brom_value),
        .pc(pc),
        .execute_from_ram(flag_execute_from_ram));

    // STAGE1
    wire[31:0] instruction_binary;
    REGISTER_up_16b r_ins_bin(
        .out(instruction_binary),
        .in(_instruction_binary),
        .clk(clk[1]));

    wire[3:0] mblock_alu_op = instruction_binary[3:0];
    wire[3:0] mblock_s1 = instruction_binary[5:4];
    wire[1:0] mblock_s2 = instruction_binary[8:6];
    wire[2:0] mblock_s3 = instruction_binary[11:9];
    wire[7:0] vrw_source = instruction_binary[23:16];
    wire[7:0] vr_source = instruction_binary[31:24];

    wire[31:0] _vr_value;
    STAGE1 stage1(
        .vr_value(_vr_value),
        .input_devices_address(input_devices_address),
        .ram_address(ram_address),
        .mblock_s1(mblock_s1),
        .vr_source(vr_source),
        .input_devices_value(input_devices_value),
        .ram_value(ram_value));

    // STAGE2
    wire[31:0] vr_value;
    REGISTER_up_16b r_ins_bin(
        .out(_vr_value),
        .in(_instruction_binary),
        .clk(clk[2]));

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