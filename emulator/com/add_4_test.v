`include "emulator/com/add_4.v"

module adder_test;
    reg[15:0] in;
    wire[15:0] out;

    ADD_4_16b dut(
        .out(out),
        .in(in));

    initial begin
        in = 2536;
        # 10
        $display("ADDER_TEST: in=%b out=%b", in, out);
        if (out !== 2540) begin
            $error("latch failed");
            $fatal(1);
        end
    end
endmodule
