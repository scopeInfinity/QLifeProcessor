`include "emulator/lib/latch.v"

module latch_d_test;
    reg I, ENABLE;
    wire O;

    latch_d dut(.out(O), .in(I), .enable(ENABLE));

    initial begin
        I = 0;
        ENABLE = 1;
        # 10
        $display("LATCH_TEST: I=%b O=%b ENABLE=%b", I, O, ENABLE);
        if (O !== 0) begin
            $error("latch failed");
            $fatal(1);
        end

        I = 1;
        ENABLE = 1;
        # 10
        $display("LATCH_TEST: I=%b O=%b ENABLE=%b", I, O, ENABLE);
        if (O !== 1) begin
            $error("latch failed");
            $fatal(1);
        end

        I = 1;
        ENABLE = 0;
        # 10
        $display("LATCH_TEST: I=%b O=%b ENABLE=%b", I, O, ENABLE);
        if (O !== 1) begin
            $error("latch failed");
            $fatal(1);
        end

        I = 0;
        ENABLE = 0;
        # 10
        $display("LATCH_TEST: I=%b O=%b ENABLE=%b", I, O, ENABLE);
        if (O !== 1) begin
            $error("latch failed");
            $fatal(1);
        end

        I = 1;
        ENABLE = 0;
        # 10
        $display("LATCH_TEST: I=%b O=%b ENABLE=%b", I, O, ENABLE);
        if (O !== 1) begin
            $error("latch failed");
            $fatal(1);
        end

        I = 0;
        ENABLE = 0;
        # 10
        $display("LATCH_TEST: I=%b O=%b ENABLE=%b", I, O, ENABLE);
        if (O !== 1) begin
            $error("latch failed");
            $fatal(1);
        end

        I = 0;
        ENABLE = 1;
        # 10
        $display("LATCH_TEST: I=%b O=%b ENABLE=%b", I, O, ENABLE);
        if (O !== 0) begin
            $error("latch failed");
            $fatal(1);
        end
    end
endmodule
