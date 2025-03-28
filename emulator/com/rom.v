`ifndef INCLUDED_ROM
`define INCLUDED_ROM

module _ROM_32bit_16aline(
        output[31:0] out,
        input[15:0] address);
    parameter filename = "/dev/null";

    reg[7:0] buffer[0:1024];
    initial begin
        $readmemb(filename, buffer);
        $display("ROM: %h", buffer[0]);
    end

    assign out[7:0] = buffer[address+0];
    assign out[15:8] = buffer[address+1];
    assign out[23:16] = buffer[address+2];
    assign out[31:24] = buffer[address+3];

endmodule

module ROM_BOOT(
        output[31:0] out,
        input[15:0] address);
    parameter filename = "emulator/com/rom_boot.bin";
    reg[15:0] eaddress;
    always @(address) begin
        eaddress = address - 'h40;
    end
    _ROM_32bit_16aline #(.filename(filename))
        _rom(.out(out),
        .address(eaddress));
endmodule

module ROM_PINGPONG(
        output[31:0] out,
        input[15:0] address);
    parameter filename = "output/programs/ping_pong.bin";
    _ROM_32bit_16aline #(.filename(filename))
        _rom(.out(out),
        .address(address));
endmodule

`endif