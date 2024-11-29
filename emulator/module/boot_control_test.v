`include "emulator/module/boot_control.v"

module boot_control_test;
    wire is_powered_on;
    BOOT_CONTROL dut(.is_powered_on(is_powered_on));

    initial begin
        # 5
        $display("BOOT_CONTROL: is_powered_on=%b", is_powered_on);
        if (is_powered_on !== 0) begin
            $error("BOOT_CONTROL failed");
            $fatal(1);
        end
        # 80
        $display("BOOT_CONTROL: is_powered_on=%b", is_powered_on);
        if (is_powered_on !== 0) begin
            $error("BOOT_CONTROL failed");
            $fatal(1);
        end
        # 20
        $display("BOOT_CONTROL: is_powered_on=%b", is_powered_on);
        if (is_powered_on !== 1) begin
            $error("BOOT_CONTROL failed");
            $fatal(1);
        end
    end
endmodule

