`include "emulator/lib/alu.v"

module alu_test;
    reg[31:0] in0, in1;
    reg[2:0] op;
    wire[31:0] out;

    ALU dut(
        .out(out),
        .op(op),
        .in0(in0),
        .in1(in1));

    initial begin
        // ADD
        op = 3'b000;
        in0 = 2536;
        in1 = 113;
        # 10
        $display("ALU_TEST: op=%b in0=%b in1=%b", op, in0, in1);
        if (out !== 2649) begin
            $error("latch failed");
            $fatal(1);
        end

        // SUB
        op = 3'b001;
        in0 = 2536;
        in1 = 113;
        # 10
        $display("ALU_TEST: op=%b in0=%b in1=%b", op, in0, in1);
        if (out !== 2423) begin
            $error("latch failed");
            $fatal(1);
        end

        // LSR
        op = 3'b010;
        in0 = 2536;
        in1 = 2;
        # 10
        $display("ALU_TEST: op=%b in0=%b in1=%b", op, in0, in1);
        if (out !== 10144) begin
            $error("latch failed");
            $fatal(1);
        end

        // RSR
        op = 3'b011;
        in0 = 2536;
        in1 = 4;
        # 10
        $display("ALU_TEST: op=%b in0=%b in1=%b", op, in0, in1);
        if (out !== 158) begin
            $error("latch failed");
            $fatal(1);
        end

    end
endmodule
