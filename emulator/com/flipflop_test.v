// `include "emulator/lib/flipflop.v"

module flipflop_test;
//     reg[31:0] in;
//     reg clk;
//     wire[31:0] out;

//     flipflop32 dut(.out(out), .in(in), .clk(clk));

//     initial begin
//         clk = 0;
//         in = 32'b00110110110101010100101101101000;
//         # 10
//         clk = 1;
//         # 10
//         $display("FLIPFLOP: in=%b out=%b clk=%b", in, out, clk);
//         if (out !== 32'b00110110110101010100101101101000) begin
//             $error("flipflop failed");
//             $fatal(1);
//         end

//         clk = 0;
//         # 10
//         in = 32'b01100011111101011011010100000100;
//         # 10
//         $display("FLIPFLOP: in=%b out=%b clk=%b", in, out, clk);
//         if (out !== 32'b00110110110101010100101101101000) begin
//             $error("flipflop failed");
//             $fatal(1);
//         end

//         in = 32'b10101100011011010010001010011001;
//         # 10
//         $display("FLIPFLOP: in=%b out=%b clk=%b", in, out, clk);
//         if (out !== 32'b00110110110101010100101101101000) begin
//             $error("flipflop failed");
//             $fatal(1);
//         end

//         clk = 1;
//         # 10
//         $display("FLIPFLOP: in=%b out=%b clk=%b", in, out, clk);
//         if (out !== 32'b10101100011011010010001010011001) begin
//             $error("flipflop failed");
//             $fatal(1);
//         end

//         clk = 0;
//         # 10
//         in = 32'b10101011001010001101001000011011;
//         # 10
//         $display("FLIPFLOP: in=%b out=%b clk=%b", in, out, clk);
//         if (out !== 32'b10101100011011010010001010011001) begin
//             $error("flipflop failed");
//             $fatal(1);
//         end
//     end
endmodule
