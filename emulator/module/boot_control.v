module BOOT_CONTROL(output is_powered_on);
    // As we don't have a button to control boot.
    // We say boot will automatically get pressed after
    // 100 time units.
    reg _is_powered_on;
    initial begin
        assign _is_powered_on = 0;
        # 100
        assign _is_powered_on = 1;
    end
    assign is_powered_on = _is_powered_on;
endmodule