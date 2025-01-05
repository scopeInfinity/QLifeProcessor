`include "emulator/com/decoder.v"

module decoder_3_test;
    reg [2:0] in;
    wire [7:0] out;

    DECODER_3 dut(.out(out), .in(in));

    initial begin
        in = 3'b010;
        # 10
        $display("DECODER_TEST: in=%b out=%b", in, out);
        if (out !== 8'b00000100) begin
            $error("decoder failed");
        end
        in = 3'b101;
        # 10
        $display("DECODER_TEST: in=%b out=%b", in, out);
        if (out !== 8'b00100000) begin
            $error("decoder failed");
        end
        in = 3'b111;
        # 10
        $display("DECODER_TEST: in=%b out=%b", in, out);
        if (out !== 8'b10000000) begin
            $error("decoder failed");
        end

    end
endmodule
