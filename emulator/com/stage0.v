`include "emulator/com/mux.v"

module STAGE0(
    output[31:0] instruction_binary,
    output[15:0] ram_address,
    output[15:0] brom_address,
    input [31:0] ram_value,
    input [31:0] brom_value,
    input [15:0] pc,
    input execute_from_ram);

    assign ram_address = pc;
    assign brom_address = pc;

    MUX_1_16b insh(
      .value(instruction_binary[31:16]),
      .A0(brom_value[31:16]),
      .A1(ram_value[31:16]),
      .S(execute_from_ram));
    MUX_1_16b insl(
      .value(instruction_binary[15:0]),
      .A0(brom_value[15:0]),
      .A1(ram_value[15:0]),
      .S(execute_from_ram));

endmodule
