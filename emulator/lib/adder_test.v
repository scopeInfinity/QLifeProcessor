`include "emulator/lib/adder.v"

module adder_test;
    reg[15:0] in0, in1;
    wire[15:0] out;

    ADDER dut(
        .out(out),
        .in0(in0),
        .in1(in1));

    initial begin
        in0 = 2536;
        in1 = 113;
        # 10
        $display("ADDER_TEST: in0=%b in1=%b", in0, in1);
        if (out !== 2649) begin
            $error("latch failed");
            $fatal(1);
        end
    end
endmodule
