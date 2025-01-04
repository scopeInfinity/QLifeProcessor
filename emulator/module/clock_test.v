`include "emulator/module/clock.v"

module clock_test;
    wire[0:3] clk;
    CLOCK dut(.clk(clk[0:3]));

    initial begin
        # 80
        # 15
        $display("CLK: clk=%b", clk);
        if (clk !== 4'b1000) begin
            $error("clock failed");
            $fatal(1);
        end
        # 20
        $display("CLK: clk=%b", clk);
        if (clk !== 4'b0100) begin
            $error("clock failed");
            $fatal(1);
        end
        # 20
        $display("CLK: clk=%b", clk);
        if (clk !== 4'b0010) begin
            $error("clock failed");
            $fatal(1);
        end
        # 20
        $display("CLK: clk=%b", clk);
        if (clk !== 4'b0001) begin
            $error("clock failed");
            $fatal(1);
        end
        $finish();
    end
endmodule

