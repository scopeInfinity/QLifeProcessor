module DECODER_4_2(
    output[3:0] out,
    input[1:0] in);

    assign out[0] = (~in[1] & ~in[0]);
    assign out[1] = (~in[1] &  in[0]);
    assign out[2] = ( in[1] & ~in[0]);
    assign out[3] = ( in[1] &  in[0]);
endmodule


module DECODER_8_3(
    output[7:0] out,
    input[2:0] in);

    wire [3:0] _out;
    DECODER_4_2 d(_out[3:0], in[1:0]);

    wire not_in2 = ~in[2];
    assign out[3:0] = _out[3:0] & {not_in2, not_in2, not_in2, not_in2};
    assign out[7:4] = _out[3:0] & {in[2], in[2], in[2], in[2]};
endmodule
