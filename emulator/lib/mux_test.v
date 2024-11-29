`include "emulator/lib/mux.v"

module mux_8_1_test;
    reg[7:0] A = 8'b01100101;
    reg[7:0] B = 8'b10101100;
    reg S;
    wire[7:0] out;

    MUX_8_1 dut(.value(out), .A(A), .B(B), .S(S));

    initial begin
        S = 0;
        # 10
        $display("MUX_TEST: A=%b B=%b S=%b OUT=%b", A, B, S, out);
        if (out !== A) begin
            $error("mux failed");
            $fatal(1);
        end
        S = 1;
        # 10
        $display("MUX_TEST: A=%b B=%b S=%b OUT=%b", A, B, S, out);
        if (out !== B) begin
            $error("mux failed");
            $fatal(1);
        end
    end
endmodule


module mux_8_2_test;
    reg[7:0] A = 8'b11101110;
    reg[7:0] B = 8'b11100110;
    reg[7:0] C = 8'b11100100;
    reg[7:0] D = 8'b00110111;
    reg[1:0] S;
    wire[7:0] out;

    MUX_8_2 dut(.value(out), .A(A), .B(B), .C(C), .D(D), .S(S));

    initial begin
        S = 0;
        # 10
        $display("MUX_TEST: A=%b B=%b S=%b OUT=%b", A, B, S, out);
        if (out !== A) begin
            $error("mux failed");
            $fatal(1);
        end
        S = 1;
        # 10
        $display("MUX_TEST: A=%b B=%b S=%b OUT=%b", A, B, S, out);
        if (out !== B) begin
            $error("mux failed");
            $fatal(1);
        end
        S = 2;
        # 10
        $display("MUX_TEST: A=%b B=%b S=%b OUT=%b", A, B, S, out);
        if (out !== C) begin
            $error("mux failed");
            $fatal(1);
        end
        S = 3;
        # 10
        $display("MUX_TEST: A=%b B=%b S=%b OUT=%b", A, B, S, out);
        if (out !== D) begin
            $error("mux failed");
            $fatal(1);
        end
    end
endmodule
