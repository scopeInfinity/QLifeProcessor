`include "emulator/module/ipc.v"

module ipc_test;
    reg[15:0] process_id;
    reg[31:0] value;

    IPCOut dut(.process_id(process_id[15:0]), .value(value[31:0]));

    initial begin
        # 5
        process_id = 10;
        # 1
        value = 20;
        # 1
        value = 25;
        # 1
        value = 30;
    end
endmodule

