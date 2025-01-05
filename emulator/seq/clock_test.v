`include "emulator/seq/clock.v"

module clock_test;
    wire[0:3] clk;
    wire[1:0] clk_stage;
    CLOCK dut(.clk(clk[0:3]), .clk_stage(clk_stage));

    initial begin
        # 80
        # 15
        $display("CLK: clk=%b, clk_stage=%b", clk, clk_stage);
        if (clk !== 4'b1000 || clk_stage !== 0) begin
            $error("clock failed");
            $fatal(1);
        end
        # 20
        $display("CLK: clk=%b, clk_stage=%b", clk, clk_stage);
        if (clk !== 4'b0100 || clk_stage !== 1) begin
            $error("clock failed");
            $fatal(1);
        end
        # 20
        $display("CLK: clk=%b, clk_stage=%b", clk, clk_stage);
        if (clk !== 4'b0010 || clk_stage !== 2) begin
            $error("clock failed");
            $fatal(1);
        end
        # 20
        $display("CLK: clk=%b, clk_stage=%b", clk, clk_stage);
        if (clk !== 4'b0001 || clk_stage !== 3) begin
            $error("clock failed");
            $fatal(1);
        end
        $finish();
    end
endmodule

