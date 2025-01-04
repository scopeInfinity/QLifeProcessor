`define BOOTSEQUENCE_ORG 'h44

module BOOT_CONTROL(
        output reg is_powered_on,
        output reg [15:0] pc_next,
        output reg [1:0] flags,
        input reset,
        input clk);

    always @(negedge clk) begin
        if(reset) begin
            flags <= 2'b00;
            pc_next <= 'h44;// BOOTSEQUENCE_ORG;
            is_powered_on <= 1;
        end
    end
endmodule