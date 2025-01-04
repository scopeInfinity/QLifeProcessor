module CLOCK(
    output[0:3] clk);

    // stages:
    //   The architecture splits instructions execution in 4 stages.
    //   stage0: fetch and expand instruction at program_counter.
    //   stage1: fetch vr_value from desidered source.
    //   stage2: fetch vrw_value from desidered source.
    //   stage3: write vw_value (result) to desidered source or pc.
    // hw_clk (internal):
    //   clock signal which controls clk[0:3]
    // clk[0],clk[1],clk[2],clk[3]:
    //   clk splitted into 4
    // The order of edges and active state.
    //   - clk[0] up
    //   - clk[0] down
    //   - clk[1] up
    //   - clk[1] down
    //   - clk[2] up
    //   - clk[2] down
    //   - clk[3] up
    //   - clk[3] down

    reg hw_clk;
    reg[0:3] _clk;
    integer _count;

    initial begin
        hw_clk = 0;
        _count = 0;
        forever begin
            #10 hw_clk = ~hw_clk;
        end
    end

    always @(posedge hw_clk) begin
      _count <= _count + 1;
      if (_count == 0) begin
        assign _clk[0] = 1;
      end
      if (_count == 1) begin
        assign _clk[1] = 1;
      end
      if (_count == 2) begin
        assign _clk[2] = 1;
      end
      if (_count == 3) begin
        assign _clk[3] = 1;
        _count <= 0;
      end
    end

    always @(negedge hw_clk) begin
      assign _clk[0:3] = 4'b0000;
    end

    assign clk[0:3] = _clk[0:3];
endmodule
