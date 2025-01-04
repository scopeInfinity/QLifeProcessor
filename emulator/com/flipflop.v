// module __flipflop #(parameter BITS = 32)(
//   output[BITS-1:0] out,
//   input clk,
//   input[BITS-1:0] in);

//   reg[BITS-1:0] mem;
//   always @(posedge clk) begin
//     mem[BITS-1:0] <= in[BITS-1:0];
//   end
//   assign out[BITS-1:0] = mem[BITS-1:0];
// endmodule

// module flipflop32(
//   output[31:0] out,
//   input clk,
//   input[31:0] in);

//   __flipflop #(.BITS(32)) ff(.out(out), .clk(clk), .in(in));

// endmodule

// module flipflop16(
//   output[15:0] out,
//   input clk,
//   input[15:0] in);

//   __flipflop #(.BITS(16)) ff(.out(out), .clk(clk), .in(in));

// endmodule

