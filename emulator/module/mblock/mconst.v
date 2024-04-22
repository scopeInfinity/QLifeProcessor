module MCONST(
        output[31:0] out,
        input[31:0] in);
    // returns constant value

    assign out[31:0] = in[31:0];

endmodule;
