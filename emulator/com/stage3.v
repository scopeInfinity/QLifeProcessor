`include "emulator/com/mux.v"
`include "emulator/com/add_4.v"
`include "emulator/com/decoder.v"

`define BOOTSEQUENCE_ORG 16'b0000000001000100

module STAGE3(
    output[31:0] output_devices_value,
    output[7:0] output_devices_address,
    output[15:0] ram_address,
    output[31:0] ram_in,
    output ram_is_write,
    output output_is_write,
    output[15:0] pc_next,
    output execute_from_ram_new,
    output is_powered_on_new,
    input[2:0] mblock_s3,
    input[31:0] vrw_value,
    input[31:0] vw_value,
    input[7:0] vrw_source,
    input[15:0] pc,
    input is_powered_on,
    input flag_last_zero,
    input execute_from_ram,
    input reset_button);

    wire[7:0] mblock_s3d;
    DECODER_3 dut(.out(mblock_s3d), .in(mblock_s3));

    assign output_devices_value = vw_value;
    assign output_devices_address = vrw_source;

    assign ram_in = vw_value;
    MUX_1_16b m1(
      .value(ram_address[15:0]),
      .A0(vrw_value[15:0]),
      .A1({8'b00000000, vrw_source[7:0]}),
      .S(mblock_s3d[1]));
    or(ram_is_write, mblock_s3d[1], mblock_s3d[3]);
    assign output_is_write = mblock_s3d[2];

    wire is_jump = (mblock_s3d[4] |
        (mblock_s3d[5] & flag_last_zero) |
        (mblock_s3d[6] & (!flag_last_zero)));
    wire[15:0] pc_4;
    ADD_4_16b add4(
        .out(pc_4),
        .in(pc));
    wire[15:0] _pc_next;
    MUX_1_16b m2(
      .value(_pc_next),
      .A0(pc_4),
      .A1(vw_value[15:0]),
      .S(is_jump));
    MUX_1_16b m3(
      .value(pc_next),
      .A0(_pc_next),
      .A1(`BOOTSEQUENCE_ORG),
      .S(reset_button));

    assign is_powered_on_new = (is_powered_on & (!mblock_s3d[7])) | reset_button;
    assign execute_from_ram_new = execute_from_ram & (!reset_button);
endmodule
