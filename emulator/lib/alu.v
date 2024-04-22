module ALU (
    output[31:0] out,
    input[2:0] op,
    input[31:0] in0,
    input[31:0] in1);

    reg[31:0] mem;

    always @(op, in0, in1) begin
        case(op)
        3'b000: mem <= in0+in1;
        3'b001: mem <= in0-in1;
        3'b010: mem <= (in0<<in1);
        3'b011: mem <= (in0>>in1);

        endcase
    end
  assign out[31:0] = mem[31:0];

endmodule
