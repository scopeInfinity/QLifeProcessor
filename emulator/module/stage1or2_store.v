module FETCH_AND_STORE(output[31:0] value,
            input[31:0] in,
            input clk);

    flipflop32 f(.out(value[31:0]), .in(in[31:0]), .clk(clk));

endmodule
