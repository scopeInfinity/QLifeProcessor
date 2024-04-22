module latch_d(output out, input in, input enable);
    // we want latch to always be on and returing
    // while write when d is active.

    reg mem;

    always @(in, enable) begin
        if (enable) begin
            mem <= in;
        end
    end
    assign out = mem;
endmodule
