`include "emulator/com/mux.v"
`include "emulator/com/stage0.v"
`include "emulator/com/stage1.v"
`include "emulator/com/stage2.v"
`include "emulator/com/stage3.v"
`include "emulator/com/rom.v"
`include "emulator/seq/clock.v"
`include "emulator/seq/register.v"
`include "emulator/seq/io_devices.v"
`include "emulator/seq/ram.v"

module CHIPSET(
    output is_powered_on,
    output[15:0] pc,
    output flag_execute_from_ram,
    input reset_button);
    // wire is_powered_on;
    // wire flag_execute_from_ram;
    wire flag_last_zero;
    // wire[15:0] pc;

    // Clock
    wire[0:3] clk;
    wire[1:0] clk_stage;
    CLOCK clock(
        .clk(clk[0:3]),
        .clk_stage(clk_stage));

    // BROM
    wire[15:0] brom_address;
    wire[31:0] brom_value;
    ROM_BOOT #(.filename("output/programs/boot_sequence.bin"))
        brom(.out(brom_value), .address(brom_address));

    // RAM
    wire ram_is_write;
    wire[15:0] ram_address;
    wire[31:0] ram_in;
    wire[31:0] ram_value;
    RAM_32bit_16aline ram(
        .out(ram_value),
        .in(ram_in),
        .address(ram_address),
        .is_write(ram_is_write),
        .clk(clk[3]));

    wire[15:0] ram_address_stage0;
    wire[15:0] ram_address_stage1;
    wire[15:0] ram_address_stage2;
    wire[15:0] ram_address_stage3;
    MUX_2_16b ram_address_selector(
      .value(ram_address),
      .A0(ram_address_stage0),
      .A1(ram_address_stage1),
      .A2(ram_address_stage2),
      .A3(ram_address_stage3),
      .S(clk_stage));
    // always @(ram_address, ram_address_stage0, ram_address_stage1, ram_address_stage2, ram_address_stage3, clk_stage)
    // begin
    // $display("add:%b, s0:%b, s1:%b, s2:%b, s3:%b, stage:%b", ram_address, ram_address_stage0, ram_address_stage1, ram_address_stage2, ram_address_stage3, clk_stage);
    // end

    // IO Devices
    wire[7:0] io_device_id_s1;
    wire[7:0] io_device_id_s3;
    wire[7:0] io_device_id;
    wire[31:0] input_devices_value;
    wire[31:0] output_devices_value;
    wire output_is_write;

    IODevices io_devices(
        .value_out(input_devices_value),
        .device_id(io_device_id),
        .value_in(output_devices_value),
        .is_write(output_is_write),
        .clk(clk[3]));

    wire[7:0] unused2;
    MUX_1_16b io_device_id_selector(
      .value({unused2, io_device_id}),
      .A0({unused2, io_device_id_s1}),
      .A1({unused2, io_device_id_s3}),
      .S(clk_stage[1]));

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
    REGISTER_up_16b stage1_r0(
        .out(instruction_binary[31:16]),
        .in(_instruction_binary[31:16]),
        .clk(clk[1]));
    REGISTER_up_16b stage1_r1(
        .out(instruction_binary[15:0]),
        .in(_instruction_binary[15:0]),
        .clk(clk[1]));

    wire[3:0] mblock_alu_op = instruction_binary[3:0];
    wire[1:0] mblock_s1 = instruction_binary[5:4];
    wire[2:0] mblock_s2 = instruction_binary[8:6];
    wire[2:0] mblock_s3 = instruction_binary[11:9];
    wire[7:0] vrw_source = instruction_binary[23:16];
    wire[7:0] vr_source = instruction_binary[31:24];

    wire[31:0] _vr_value;
    STAGE1 stage1(
        .vr_value(_vr_value),
        .io_device_id(io_device_id_s1),
        .ram_address(ram_address_stage1),
        .mblock_s1(mblock_s1),
        .vr_source(vr_source),
        .input_devices_value(input_devices_value),
        .ram_value(ram_value));

    // STAGE2
    wire[31:0] vr_value;
    REGISTER_up_16b stage2_r0(
        .out(vr_value[31:16]),
        .in(_vr_value[31:16]),
        .clk(clk[2]));
    REGISTER_up_16b stage2_r1(
        .out(vr_value[15:0]),
        .in(_vr_value[15:0]),
        .clk(clk[2]));

    wire[31:0] _vrw_value;
    wire[31:0] _vw_value;
    wire _alu_is_zero;
    STAGE2 stage2(
        .vrw_value(_vrw_value),
        .vw_value(_vw_value),
        .ram_address(ram_address_stage2),
        .alu_is_zero(_alu_is_zero),
        .mblock_s2(mblock_s2),
        .vr_source(vr_source),
        .vr_value(vr_value),
        .vrw_source(vrw_source),
        .alu_op(mblock_alu_op),
        .pc(pc),
        .ram_value(ram_value));

    // STAGE3
    wire[31:0] vrw_value;
    wire[31:0] vw_value;
    wire alu_is_zero;
    REGISTER_up_16b stage3_r0a(
        .out(vrw_value[31:16]),
        .in(_vrw_value[31:16]),
        .clk(clk[3]));
    REGISTER_up_16b stage3_r0b(
        .out(vrw_value[15:0]),
        .in(_vrw_value[15:0]),
        .clk(clk[3]));
    REGISTER_up_16b stage3_r1a(
        .out(vw_value[31:16]),
        .in(_vw_value[31:16]),
        .clk(clk[3]));
    REGISTER_up_16b stage3_r1b(
        .out(vw_value[15:0]),
        .in(_vw_value[15:0]),
        .clk(clk[3]));
    wire[14:0] unused0;
    REGISTER_up_16b stage3_r2(
        .out({unused0, alu_is_zero}),
        .in({15'bzzzzzzzzzzzzzzz, _alu_is_zero}),
        .clk(clk[3]));


    wire execute_from_ram_new;
    wire is_powered_on_new;
    wire[15:0] pc_next;

    STAGE3 stage3(
        .output_devices_value(output_devices_value),
        .io_device_id(io_device_id_s3),
        .ram_address(ram_address_stage3),
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
        .execute_from_ram(flag_execute_from_ram),
        .reset_button(reset_button));

    wire[12:0] unused1;
    REGISTER_down_16b stage3_r3(
        .out({unused1, flag_last_zero, is_powered_on, flag_execute_from_ram}),
        .in({13'bzzzzzzzzzzzzz, alu_is_zero, is_powered_on_new, execute_from_ram_new}),
        .clk(clk[3]));

    REGISTER_down_16b stage3_r4(
        .out(pc),
        .in(pc_next),
        .clk(clk[3]));

    // always @(negedge clk[0]) begin
    //     $display("Stage0: power=%b pc=%x ins=%b eram=%b",
    //         is_powered_on_new, pc, _instruction_binary, flag_execute_from_ram);
    // end
    // always @(negedge clk[1]) begin
    //     $display("Stage1: alu=%b s1=%b s2=%b s3=%b vrw_source=%x vr_source=%x",
    //         mblock_alu_op, mblock_s1, mblock_s2, mblock_s3, vrw_source, vr_source);
    // end
    // always @(negedge clk[2]) begin
    //     $display("Stage2: vr_value=%x",
    //         vr_value);
    // end
    // always @(negedge clk[3]) begin
    //     $display("Stage3: vrw_value=%x, vw_value=%x is_zero=%b",
    //         vrw_value, vw_value, alu_is_zero);
    // end
    // always @(posedge clk[0]) begin
    //     $display("StageE: power=%b, f_zero=%b, f_eram=%b pc=%x write_ram=%b wrire_io=%b",
    //         is_powered_on, flag_last_zero, flag_execute_from_ram, pc, ram_is_write, output_is_write);
    // end
endmodule