`include "emulator/module/ipc.v"

module ipc_out_test;
    reg[7:0] device_id;
    reg[31:0] value;

    IPCOut dut(.device_id(device_id[7:0]), .value(value[31:0]));

    initial begin
        # 5
        device_id = 10;
        # 1
        value = 20;
        // Not test here, output goes to stdout.
    end
endmodule

module ipc_in_test;
    reg[7:0] device_id;
    reg clk;
    output[31:0] value;

    IPCIn dut(.value(value[31:0]), .device_id(device_id[7:0]), .clk(clk));

    integer f;
    initial begin
        # 5
        f = $fopen("/tmp/ourpc_input", "w");
        $fwrite(f,"00000000000000000000000000000001\n");
        $fwrite(f,"11111111111111111111111111111111\n");
        $fwrite(f,"01010101010101010101010101010101\n");
        $fwrite(f,"10101010101010101010101010101010\n");
        $fwrite(f,"00000000000000000000000011111111\n");
        $fwrite(f,"11111111000000000000000000000000\n");
        $fwrite(f,"01010101101010100101010110101010\n");
        $fwrite(f,"10101010010101011010101001010101\n");
        $fclose(f);

        device_id = 1;
        clk = 0;
        # 5
        clk = 1;
        # 5
        if (value !== 32'b11111111111111111111111111111111) begin
            $error("ipc input failed, got: %b", value);
            $fatal(1);
        end
        device_id = 6;
        # 1
        if (value !== 32'b01010101101010100101010110101010) begin
            $error("ipc input failed, got: %b", value);
            $fatal(1);
        end

    end
endmodule

