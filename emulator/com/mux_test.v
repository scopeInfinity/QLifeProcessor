`include "emulator/com/mux.v"

module mux_1_test;
    reg[15:0] A0 = 16'b0110010101100101;
    reg[15:0] A1 = 16'b1010110010101100;
    reg S;
    wire[15:0] out;

    MUX_1_16b dut(.value(out), .A0(A0), .A1(A1), .S(S));

    initial begin
        S = 0;
        # 10
        $display("MUX_TEST: A0=%b A1=%b S=%b OUT=%b", A0, A1, S, out);
        if (out !== A0) begin
            $error("mux failed");
            $fatal(1);
        end
        S = 1;
        # 10
        $display("MUX_TEST: A0=%b A1=%b S=%b OUT=%b", A0, A1, S, out);
        if (out !== A1) begin
            $error("mux failed");
            $fatal(1);
        end
    end
endmodule

module mux_2_test;
    reg[15:0] A0 = 16'b0110010101100101;
    reg[15:0] A1 = 16'b1010110010101100;
    reg[15:0] A2 = 16'b1010001001010101;
    reg[15:0] A3 = 16'b0101010101010100;
    reg[1:0] S;
    wire[15:0] out;

    MUX_2_16b dut(.value(out), .A0(A0), .A1(A1), .A2(A2), .A3(A3), .S(S));

    initial begin
        S = 2'b00;
        # 10
        $display("MUX_TEST: A0=%b A1=%b A1=%b A1=%b S=%b OUT=%b", A0, A1, S, out);
        if (out !== A0) begin
            $error("mux failed");
            $fatal(1);
        end
        S = 2'b01;
        # 10
        $display("MUX_TEST: A0=%b A1=%b S=%b OUT=%b", A0, A1, S, out);
        if (out !== A1) begin
            $error("mux failed");
            $fatal(1);
        end
        S = 2'b10;
        # 10
        $display("MUX_TEST: A0=%b A1=%b S=%b OUT=%b", A0, A1, S, out);
        if (out !== A2) begin
            $error("mux failed");
            $fatal(1);
        end
        S = 2'b11;
        # 10
        $display("MUX_TEST: A0=%b A1=%b S=%b OUT=%b", A0, A1, S, out);
        if (out !== A3) begin
            $error("mux failed");
            $fatal(1);
        end
    end
endmodule
