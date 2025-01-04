`include "emulator/module/boot_control.v"

module boot_control_test;
    // reg reset;

    // reg is_powered_on;
    // reg[15:0] pc_next;
    // reg[1:0] flags;
    // reg clk;

    // BOOT_CONTROL dut(
    //     .is_powered_on(is_powered_on),
    //     .pc_next(pc_next),
    //     .flags(flags),
    //     .reset(reset),
    //     .clk(clk));

    // initial begin
    //     # 5
    //     clk = 1;
    //     # 1
    //     reset = 1;
    //     # 1
    //     clk = 0;
    //     # 1
    //     reset = 0;
    //     $display("BOOT_CONTROL: is_powered_on=%b, pc_next=%b, flags: %b",
    //         is_powered_on, pc_next, flags);
    //     if (is_powered_on !== 0 || pc_next !== 'h80 || flags !== 0) begin
    //         $error("BOOT_CONTROL failed");
    //         $fatal(1);
    //     end
    // end
endmodule

