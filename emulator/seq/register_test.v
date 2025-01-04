`include "emulator/seq/register.v"

module register_up_test;
    reg[15:0] in = 16'b0110010101100101;
    reg clk;
    wire[15:0] out;

    REGISTER_up_16b dut(.out(out), .in(in), .clk(clk));

    initial begin
        clk = 0;
        # 10
        clk = 1;
        # 1
        clk = 0;
        # 1
        in = 16'b1010110010101100;
        # 1
        $display("REGISTER_UP_TEST: in=%b out=%b clk=%b", in, out, clk);
        if (out !== 16'b0110010101100101) begin // old value
            $error("register failed");
            $fatal(1);
        end
        clk = 1;
        # 10
        $display("REGISTER_UP_TEST: in=%b out=%b clk=%b", in, out, clk);
        if (out !== 16'b1010110010101100) begin
            $error("register failed");
            $fatal(1);
        end
    end
endmodule

module register_down_test;
    reg[15:0] in = 16'b0110010101100101;
    reg clk;
    wire[15:0] out;

    REGISTER_down_16b dut(.out(out), .in(in), .clk(clk));

    initial begin
        clk = 1;
        # 10
        clk = 0;
        # 1
        clk = 1;
        # 1
        in = 16'b1010110010101100;
        # 1
        $display("REGISTER_DOWN_TEST: in=%b out=%b clk=%b", in, out, clk);
        if (out !== 16'b0110010101100101) begin // old value
            $error("register failed");
            $fatal(1);
        end
        clk = 0;
        # 10
        $display("REGISTER_DOWN_TEST: in=%b out=%b clk=%b", in, out, clk);
        if (out !== 16'b1010110010101100) begin
            $error("register failed");
            $fatal(1);
        end
    end
endmodule
