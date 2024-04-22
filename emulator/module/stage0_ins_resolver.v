module INS_RESOLVER(output[7:0] v0, v1, v2, op,
            input[32:0] full_ins,
            input clk);

    wire[31:0] mem_ins;
    flipflop32 f(.out(mem_ins[31:0]), .in(full_ins[31:0]), .clk(clk));

    assign v0[7:0] = full_ins[ 7: 0];
    assign v1[7:0] = full_ins[15: 8];
    assign v2[7:0] = full_ins[23:16];
    assign op[7:0] = full_ins[31:24];

endmodule;
