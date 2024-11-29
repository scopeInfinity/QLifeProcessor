// MUX 8-bit IO with 1-bit selection
// B is returned when S is active.
module MUX_8_1(
    output [7:0] value,
    input[7:0] A,B,
    input S);

    wire Snot;
    not (Snot, S);

    wire [7:0] x;
    wire [7:0] y;
    and (x[0], A[0], Snot);
    and (x[1], A[1], Snot);
    and (x[2], A[2], Snot);
    and (x[3], A[3], Snot);
    and (x[4], A[4], Snot);
    and (x[5], A[5], Snot);
    and (x[6], A[6], Snot);
    and (x[7], A[7], Snot);


    and (y[0], B[0], S);
    and (y[1], B[1], S);
    and (y[2], B[2], S);
    and (y[3], B[3], S);
    and (y[4], B[4], S);
    and (y[5], B[5], S);
    and (y[6], B[6], S);
    and (y[7], B[7], S);

    or (value[0], x[0], y[0]);
    or (value[1], x[1], y[1]);
    or (value[2], x[2], y[2]);
    or (value[3], x[3], y[3]);
    or (value[4], x[4], y[4]);
    or (value[5], x[5], y[5]);
    or (value[6], x[6], y[6]);
    or (value[7], x[7], y[7]);

endmodule

module MUX_8_2(
    output[7:0] value,
    input[7:0] A,B,C,D,
    input[1:0] S);

    wire[7:0] val_a, val_b;

    MUX_8_1 m1(.value(val_a), .A(A), .B(B), .S(S[0]));
    MUX_8_1 m2(.value(val_b), .A(C), .B(D), .S(S[0]));
    MUX_8_1 m3(.value(value), .A(val_a), .B(val_b), .S(S[1]));

endmodule

