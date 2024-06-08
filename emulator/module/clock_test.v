`include "emulator/module/clock.v"

module clock_test;
    wire[0:3] clk;
    wire[0:3] is_stage;
    CLOCK dut(
        .clk(clk[0:3]),
        .is_stage(is_stage[0:3]));

    initial begin
        # 75
        $display("CLK: clk=%b is_stage=%b", clk, is_stage);
        if (clk !== 4'b0001 || is_stage !== 4'b1000) begin
            $error("clock failed");
            $fatal(1);
        end
        # 20
        $display("CLK: clk=%b is_stage=%b", clk, is_stage);
        if (clk !== 4'b1000 || is_stage !== 4'b0100) begin
            $error("clock failed");
            $fatal(1);
        end
        # 20
        $display("CLK: clk=%b is_stage=%b", clk, is_stage);
        if (clk !== 4'b0100 || is_stage !== 4'b0010) begin
            $error("clock failed");
            $fatal(1);
        end
        # 20
        $display("CLK: clk=%b is_stage=%b", clk, is_stage);
        if (clk !== 4'b0010 || is_stage !== 4'b0001) begin
            $error("clock failed");
            $fatal(1);
        end
        # 20
        $display("CLK: clk=%b is_stage=%b", clk, is_stage);
        if (clk !== 4'b0001 || is_stage !== 4'b1000) begin
            $error("clock failed");
            $fatal(1);
        end
        $finish();
    end
endmodule

