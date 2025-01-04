module REGISTER_up_16b(
    output [15:0] out,
    input [15:0] in,
    input clk);

    reg [15:0] _data;
    always @(posedge clk) begin
        _data = in;
    end
    assign out = _data;
endmodule

module REGISTER_down_16b(
    output [15:0] out,
    input [15:0] in,
    input clk);

    reg [15:0] _data;
    always @(negedge clk) begin
        _data = in;
    end
    assign out = _data;
endmodule
