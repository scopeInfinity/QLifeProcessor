`include "emulator/lib/alu.v"

module alu_test;
    reg[31:0] in0, in1;
    reg[2:0] op;
    wire[31:0] out;
    wire is_zero;

    ALU dut(
        .out(out),
        .is_zero(is_zero),
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
        if (out !== 2649 || is_zero !== 0) begin
            $error("alu failed");
            $fatal(1);
        end

        // SUB
        op = 3'b001;
        in0 = 2536;
        in1 = 113;
        # 10
        $display("ALU_TEST: op=%b in0=%b in1=%b", op, in0, in1);
        if (out !== 2423 || is_zero !== 0) begin
            $error("alu failed");
            $fatal(1);
        end

        // LSR
        op = 3'b010;
        in0 = 2536;
        in1 = 2;
        # 10
        $display("ALU_TEST: op=%b in0=%b in1=%b", op, in0, in1);
        if (out !== 10144 || is_zero !== 0) begin
            $error("alu failed");
            $fatal(1);
        end

        // RSR
        op = 3'b011;
        in0 = 2536;
        in1 = 4;
        # 10
        $display("ALU_TEST: op=%b in0=%b in1=%b", op, in0, in1);
        if (out !== 158 || is_zero !== 0) begin
            $error("alu failed");
            $fatal(1);
        end

        // Fist Operand
        op = 3'b100;
        in0 = 2536;
        in1 = 4;
        # 10
        $display("ALU_TEST: op=%b in0=%b in1=%b", op, in0, in1);
        if (out !== 2536 || is_zero !== 0) begin
            $error("alu failed");
            $fatal(1);
        end

        // CMP as alias of SUB
        op = 3'b001;
        in0 = 2536;
        in1 = 2536;
        # 10
        $display("ALU_TEST: op=%b in0=%b in1=%b", op, in0, in1);
        if (out !== 0 || is_zero !== 1) begin
            $error("alu failed");
            $fatal(1);
        end

        // AND
        op = 3'b101;
        in0 = 2536;
        in1 = 113;
        # 10
        $display("ALU_TEST: op=%b in0=%b in1=%b", op, in0, in1);
        if (out !== 96 || is_zero !== 0) begin
            $error("alu failed");
            $fatal(1);
        end

        // OR
        op = 3'b110;
        in0 = 2536;
        in1 = 3113;
        # 10
        $display("ALU_TEST: op=%b in0=%b in1=%b", op, in0, in1);
        if (out !== 3561 || is_zero !== 0) begin
            $error("alu failed");
            $fatal(1);
        end

    end
endmodule
