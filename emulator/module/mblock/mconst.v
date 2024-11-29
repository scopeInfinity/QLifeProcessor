module MCONST(
        output[31:0] out,
        input[15:0] in);
    // returns constant value

    assign out[31:16] = 16'b0000000000000000;
    assign out[15:0] = in[15:0];

endmodule
