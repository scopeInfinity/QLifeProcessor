`include "emulator/lib/decoder.v"

module decoder_4_2_test;
    reg [1:0] in;
    wire [3:0] out;

    DECODER_4_2 dut(.out(out), .in(in));

    initial begin
        in = 2'b00;
        # 10
        $display("DECODER_TEST: in=%b out=%b", in, out);
        if (out != 4'b0001) begin
            $error("decoder failed");
        end
        in = 2'b01;
        # 10
        $display("DECODER_TEST: in=%b out=%b", in, out);
        if (out != 4'b0010) begin
            $error("decoder failed");
        end
        in = 2'b10;
        # 10
        $display("DECODER_TEST: in=%b out=%b", in, out);
        if (out != 4'b0100) begin
            $error("decoder failed");
        end
        in = 2'b11;
        # 10
        $display("DECODER_TEST: in=%b out=%b", in, out);
        if (out != 4'b1000) begin
            $error("decoder failed");
        end

    end
endmodule


module decoder_8_3_test;
    reg [2:0] in;
    wire [7:0] out;

    DECODER_8_3 dut(.out(out), .in(in));

    initial begin
        in = 3'b010;
        # 10
        $display("DECODER_TEST: in=%b out=%b", in, out);
        if (out != 8'b00000100) begin
            $error("decoder failed");
            $fatal(1);
        end
        in = 3'b101;
        # 10
        $display("DECODER_TEST: in=%b out=%b", in, out);
        if (out != 8'b00100000) begin
            $error("decoder failed");
            $fatal(1);
        end
    end
endmodule
