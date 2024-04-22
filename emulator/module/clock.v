module CLOCK(
    output clk,
    output clk0,
    output clk1,
    output clk2,
    output clk3,
    output is_stage0,
    output is_stage1,
    output is_stage2,
    output is_stage3);

    // stages:
    //   The architecture splits instructions execution in 4 stages.
    //   stage0: fetch and expand instruction at program_counter.
    //   stage1: fetch value0 (usually operand0) from desidered source.
    //   stage2: fetch value1 (usually operand1) from desidered source.
    //   stage3: write value2 (result) to desidered source and update
    //           program_counter if and when desired.
    // clk:
    //   clock signal
    // clk0,clk1,clk2,clk3:
    //   clk splitted into 4. Each clk{i} posedge represents flipflop write
    //   of stage{i}.
    //   e.g. stage1 is active b/w clk0 and clk1 posedge.

    // TODO: Implement it.

endmodule;

