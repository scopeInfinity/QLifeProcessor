module ADDER(
    output[15:0] out,
    input[15:0] in0,
    input[15:0] in1);

    assign out = in0+in1;
endmodule
