`include "emulator/module/mblock/mconst.v"

module MCONST_test;
    reg[31:0] in;
    wire[31:0] out;

    MCONST dut(.out(out),
        .in(in));

    initial begin
        in = 32'b00011100100011110010111100010010;
        # 10
        $display("MCONST_TEST: in=%b out=%b", in, out);
        if (out !== 32'b00011100100011110010111100010010) begin
            $error("mconst failed");
            $fatal(1);
        end
        in = 32'b00111110011011111001011000011000;
        # 10
        $display("MCONST_TEST: in=%b out=%b", in, out);
        if (out !== 32'b00111110011011111001011000011000) begin
            $error("mconst failed");
            $fatal(1);
        end
    end
endmodule
