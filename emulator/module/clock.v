module CLOCK(
    output[0:3] clk,
    output[0:3] is_stage);

    // stages:
    //   The architecture splits instructions execution in 4 stages.
    //   stage0: fetch and expand instruction at program_counter.
    //   stage1: fetch value0 (usually operand0) from desidered source.
    //   stage2: fetch value1 (usually operand1) from desidered source.
    //   stage3: write value2 (result) to desidered source and update
    //           program_counter if and when desired.
    // hw_clk (internal):
    //   clock signal
    // clk[0],clk[1],clk[2],clk[3]:
    //   clk splitted into 4. Each clk{i} posedge represents flipflop write
    //   of stage{i}.
    //   e.g. stage1 is active b/w clk0 and clk1 posedge.


    // TODO: make clock more realistic.
    reg[0:3] hw_clk;
    reg[0:3] _is_stage;
    initial begin
      forever begin
        #10
        _is_stage[0]=0;
        hw_clk[0]=1;
        _is_stage[1]=1;
        #10
        hw_clk[0]=0;
        #10
        _is_stage[1]=0;
        hw_clk[1]=1;
        _is_stage[2]=1;
        #10
        hw_clk[1]=0;
        #10
        _is_stage[2]=0;
        hw_clk[2]=1;
        _is_stage[3]=1;
        #10
        hw_clk[2]=0;
        #10
        _is_stage[3]=0;
        hw_clk[3]=1;
        _is_stage[0]=1;
        #10
        hw_clk[3]=0;
      end
    end

    assign clk[0:3] = hw_clk[0:3];
    assign is_stage[0:3] = _is_stage[0:3];
endmodule
