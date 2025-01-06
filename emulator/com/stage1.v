`include "emulator/com/mux.v"

module STAGE1(
    output[31:0] vr_value,
    output[7:0] io_device_id,
    output[15:0] ram_address,
    input[1:0] mblock_s1,
    input[7:0] vr_source,
    input[31:0] input_devices_value,
    input[31:0] ram_value);

    wire[31:0] _const_value;

    assign io_device_id = vr_source;
    assign _const_value[7:0] = vr_source;
    assign _const_value[31:8] = 24'b000000000000000000000000;
    assign ram_address[7:0] = vr_source;
    assign ram_address[15:8] = 8'b00000000;

    MUX_2_16b m1(
      .value(vr_value[31:16]),
      .A0(ram_value[31:16]),
      .A1(16'bxxxxxxxxxxxxxxxx),
      .A2(input_devices_value[31:16]),
      .A3(_const_value[31:16]),
      .S(mblock_s1));

    MUX_2_16b m2(
      .value(vr_value[15:0]),
      .A0(ram_value[15:0]),
      .A1(16'bxxxxxxxxxxxxxxxx),
      .A2(input_devices_value[15:0]),
      .A3(_const_value[15:0]),
      .S(mblock_s1));

endmodule
