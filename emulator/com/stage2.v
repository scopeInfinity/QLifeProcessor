`include "emulator/com/mux.v"
`include "emulator/com/alu.v"

module STAGE2(
    output[31:0] vrw_value,
    output[31:0] vw_value,
    output[15:0] ram_address,
    output alu_is_zero,
    input[2:0] mblock_s2,
    input[7:0] vr_source,
    input[31:0] vr_value,
    input[7:0] vrw_source,
    input[3:0] alu_op,
    input[15:0] pc,
    input[31:0] ram_value);

    wire[15:0] _iv;
    wire[31:0] _m_vrw_value;

    MUX_2_16b m1(
      .value(_iv[15:0]),
      .A0({8'b00000000, vrw_source[7:0]}),
      .A1(vr_value[15:0]),
      .A2({vr_source[7:0], vrw_source[7:0]}),
      .A3(16'bxxxxxxxxxxxxxxxx),
      .S(mblock_s2[1:0]));

    assign ram_address = _iv;

    MUX_1_16b m2a(
      .value(_m_vrw_value[31:16]),
      .A0(ram_value[31:16]),
      .A1(16'b0000000000000000),
      .S(mblock_s2[2]));
    MUX_1_16b m2b(
      .value(_m_vrw_value[15:0]),
      .A0(ram_value[15:0]),
      .A1(_iv[15:0]),
      .S(mblock_s2[2]));

    wire want_pc = (
        mblock_s2[0] & mblock_s2[1] & mblock_s2[2]
    );

    MUX_1_16b m3a(
      .value(vrw_value[31:16]),
      .A0(_m_vrw_value[31:16]),
      .A1(16'b0000000000000000),
      .S(want_pc));
    MUX_1_16b m3b(
      .value(vrw_value[15:0]),
      .A0(_m_vrw_value[15:0]),
      .A1(pc[15:0]),
      .S(want_pc));

    ALU alu(
        .out(vw_value),
        .is_zero(alu_is_zero),
        .op(alu_op),
        .in_r(vr_value),
        .in_rw(vrw_value));

endmodule
