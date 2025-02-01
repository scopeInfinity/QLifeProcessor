`define ALU_OP_ADD 4'b0000


module ALU (
    output[31:0] out,
    output is_zero,
    input[3:0] op,
    input[31:0] in_r,
    input[31:0] in_rw);

    reg[31:0] mem;

    always @(op, in_r, in_rw) begin
        case(op)
        4'b0000: mem = in_r+in_rw;
        4'b0001: mem = in_rw-in_r;
        4'b0010: mem = (in_rw<<in_r);
        4'b0011: mem = (in_rw>>in_r);
        4'b0100: mem = (in_r);
        4'b0101: mem = (in_rw);
        4'b0110: mem = (in_r&in_rw);
        4'b0111: mem = (in_r|in_rw);
        4'b1000: mem = (in_r^in_rw);
        4'b1001: mem = (((in_r&255)<<8)|in_rw&255);
        endcase
    end
  assign out[31:0] = mem[31:0];
  assign is_zero = (mem == 0);

endmodule
