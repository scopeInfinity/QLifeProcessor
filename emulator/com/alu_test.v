`include "emulator/com/alu.v"

module alu_test;
    reg[31:0] in_r, in_rw;
    reg[3:0] op;
    wire[31:0] out;
    wire is_zero;

    ALU dut(
        .out(out),
        .is_zero(is_zero),
        .op(op),
        .in_r(in_r),
        .in_rw(in_rw));

    initial begin
        // ADD
        op = 4'b0000;
        in_r = 2536;
        in_rw = 113;
        # 10
        $display("ALU_TEST: op=%b in_r=%b in_rw=%b", op, in_r, in_rw);
        if (out !== 2649 || is_zero !== 0) begin
            $error("alu failed");
            $fatal(1);
        end

        // SUB
        op = 4'b0001;
        in_r = 2536;
        in_rw = 113;
        # 10
        $display("ALU_TEST: op=%b in_r=%b in_rw=%b", op, in_r, in_rw);
        if (out !== 2423 || is_zero !== 0) begin
            $error("alu failed");
            $fatal(1);
        end

        // LSR
        op = 4'b0010;
        in_r = 2536;
        in_rw = 2;
        # 10
        $display("ALU_TEST: op=%b in_r=%b in_rw=%b", op, in_r, in_rw);
        if (out !== 10144 || is_zero !== 0) begin
            $error("alu failed");
            $fatal(1);
        end

        // RSR
        op = 4'b0011;
        in_r = 2536;
        in_rw = 4;
        # 10
        $display("ALU_TEST: op=%b in_r=%b in_rw=%b", op, in_r, in_rw);
        if (out !== 158 || is_zero !== 0) begin
            $error("alu failed");
            $fatal(1);
        end

        // Fist Operand
        op = 4'b0100;
        in_r = 2536;
        in_rw = 4;
        # 10
        $display("ALU_TEST: op=%b in_r=%b in_rw=%b", op, in_r, in_rw);
        if (out !== 2536 || is_zero !== 0) begin
            $error("alu failed");
            $fatal(1);
        end

        // Second Operand
        op = 4'b0101;
        in_r = 2536;
        in_rw = 4;
        # 10
        $display("ALU_TEST: op=%b in_r=%b in_rw=%b", op, in_r, in_rw);
        if (out !== 4 || is_zero !== 0) begin
            $error("alu failed");
            $fatal(1);
        end

        // AND
        op = 4'b0110;
        in_r = 2536;
        in_rw = 113;
        # 10
        $display("ALU_TEST: op=%b in_r=%b in_rw=%b", op, in_r, in_rw);
        if (out !== 96 || is_zero !== 0) begin
            $error("alu failed");
            $fatal(1);
        end

        // OR
        op = 4'b0111;
        in_r = 2536;
        in_rw = 3113;
        # 10
        $display("ALU_TEST: op=%b in_r=%b in_rw=%b", op, in_r, in_rw);
        if (out !== 3561 || is_zero !== 0) begin
            $error("alu failed");
            $fatal(1);
        end

        // XOR
        op = 4'b1000;
        in_r = 2536;
        in_rw = 3113;
        # 10
        $display("ALU_TEST: op=%b in_r=%b in_rw=%b", op, in_r, in_rw);
        if (out !== 1473 || is_zero !== 0) begin
            $error("alu failed");
            $fatal(1);
        end

        // R_SHL8_RW_OR
        op = 4'b01001;
        in_r = 213;
        in_rw = 123;
        # 10
        $display("ALU_TEST: op=%b in_r=%b in_rw=%b", op, in_r, in_rw);
        if (out !== 54651 || is_zero !== 0) begin
            $error("alu failed");
            $fatal(1);
        end

    end
endmodule
