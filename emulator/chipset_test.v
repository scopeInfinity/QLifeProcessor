`include "emulator/chipset.v"

module chipset_test;
    reg reset_button;

    wire is_powered_on;
    wire flag_execute_from_ram;
    wire[15:0] pc;
    CHIPSET dut(
        .reset_button(reset_button),
        .pc(pc),
        .is_powered_on(is_powered_on),
        .flag_execute_from_ram(flag_execute_from_ram));

    initial begin
        reset_button = 0;
        # 80
        reset_button = 1;
        # 80
        reset_button = 0;
        # 200000
        if (reset_button !== 0) begin
            $error("chipset failed");
            $fatal(1);
        end
        $finish();
    end
endmodule
