module PC_NEXT(
    inout [15:0] program_counter,
    input is_powered_on,
    input clk);

    // TODO: we should support jmp like instructions.

    wire[15:0] program_counter_plus_one;
    wire[15:0] program_counter_next;

    ADDER pc_adder(
            .out(program_counter_plus_one),
            .in0(program_counter),
            .in1(1));

    AND(program_counter_next[00], program_counter_plus_one[00], is_powered_on);
    AND(program_counter_next[01], program_counter_plus_one[01], is_powered_on);
    AND(program_counter_next[02], program_counter_plus_one[02], is_powered_on);
    AND(program_counter_next[03], program_counter_plus_one[03], is_powered_on);
    AND(program_counter_next[04], program_counter_plus_one[04], is_powered_on);
    AND(program_counter_next[05], program_counter_plus_one[05], is_powered_on);
    AND(program_counter_next[06], program_counter_plus_one[06], is_powered_on);
    AND(program_counter_next[07], program_counter_plus_one[07], is_powered_on);
    AND(program_counter_next[08], program_counter_plus_one[08], is_powered_on);
    AND(program_counter_next[09], program_counter_plus_one[09], is_powered_on);
    AND(program_counter_next[10], program_counter_plus_one[10], is_powered_on);
    AND(program_counter_next[11], program_counter_plus_one[11], is_powered_on);
    AND(program_counter_next[12], program_counter_plus_one[12], is_powered_on);
    AND(program_counter_next[13], program_counter_plus_one[13], is_powered_on);
    AND(program_counter_next[14], program_counter_plus_one[14], is_powered_on);
    AND(program_counter_next[15], program_counter_plus_one[15], is_powered_on);

    flipflop16 pc(
        .out(program_counter),
        .in(program_counter_next),
        .clk(clk));
endmodule
