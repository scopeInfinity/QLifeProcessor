module _ROM_32bit_16aline(
        output[31:0] out,
        input[15:0] address);
    // 4 * 64KB ROM

    parameter filename = "/dev/null";

    reg[31:0] buffer[0:65535];
    initial begin
        $readmemb(filename, buffer);
        $display("ROM: %h", buffer[0]);
    end

    assign out = buffer[address];

endmodule;

module ROM_BOOT(
        output[31:0] out,
        input[15:0] address);
    // 4 * 64KB ROM

    _ROM_32bit_16aline #(.filename("emulator/module/mblock/rom_boot.bin"))
        dut(.out(out),
        .address(address));
endmodule;
