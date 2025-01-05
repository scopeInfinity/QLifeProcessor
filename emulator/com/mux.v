`ifndef INCLUDED_MUX
`define INCLUDED_MUX

module MUX_1_16b(
    output reg [15:0] value,
    input [15:0] A0, A1,
    input S);

    always @(*) begin
        if (S) begin
            value = A1;
        end else begin
            value = A0;
        end
    end
endmodule

module MUX_2_16b(
    output reg [15:0] value,
    input [15:0] A0, A1, A2, A3,
    input [1:0] S);

    always @(*) begin
        case (S)
            2'b00: value = A0;
            2'b01: value = A1;
            2'b10: value = A2;
            2'b11: value = A3;
        endcase
    end
endmodule
`endif