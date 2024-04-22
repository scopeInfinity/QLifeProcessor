`include "emulator/module/clock.v"

module CHIPSET();
    // Global Registers
    reg execute_from_brom;

    // Stages
    wire clk, clk0, clk1, clk2, clk3;
    CLOCK clock(
        .clk(clk),
        .clk0(clk0),
        .clk0(clk1),
        .clk0(clk2),
        .clk0(clk3),
        .is_stage0(is_stage0),
        .is_stage1(is_stage1),
        .is_stage2(is_stage2),
        .is_stage3(is_stage3));

    // Boot Sequence
    //
    // When the device have power supply but `is_powered_on` is off. The pc_eval
    // forces `program_counter_next` to be 0 and `execute_from_brom` to True.
    // If we keep the `is_powered_on` button in off stage for at-least 4 cycles
    // then at "stage3 posedge" program_counter should get updated to 0.
    // After that for every "stage0 posedge" till is_powered_on is off,
    // program_counter:0 along with execute_from_brom:True will be used to pull
    // up and execute first instruction from BROM.
    //
    // Assumption: No stateful IO devices are connected.
    // TODO: Implement `execute_from_brom` update implementation.
    wire is_powered_on;
    BOOT_CONTROL boot_control(.is_powered_on(is_powered_on));


    // MBLOCK is a continous circuit and doesn't depend on clock
    // but the behaviour do depend on stage which is abstracted.
    wire[15:0] program_counter;
    wire[1:0] mblock_selector;
    wire[15:0] mblock_address;
    wire[31:0] mblock_input;
    wire[31:0] mblock_output;
    wire mblock_write;

    MBLOCK_MUX mblock_mux(
        .mblock_address(mblock_address[15:0]),
        .mblock_selector(mblock_selector[1:0]),
        .address0(program_counter),
        .address1(v0_source),
        .address2(v1_source),
        .address3(v2_source),
        .is_stage0(is_stage0),
        .is_write0(0),
        .is_write1(0),
        .is_write2(0),
        .is_write3(0));

    MBLOCK mblock(
        .out(mblock_output),
        .selector(mblock_selector),
        .in(mblock_input),
        .address(mblock_address),
        .is_write(mblock_write));

    // STAGE0

    // TODO: Ensure MBLOCK supplies expectations.
    // MBLOCK_MUX is expected to fetch MBLOCK at `program_counter` from
    // BROM / RAM based on `execute_from_brom` and redirect the value
    // to full_ins via mblock_output.

    // @stage0 posedge following values should freeze.
    wire[7:0] v0_source, v1_source, v2_source, instruction_op;
    INS_RESOLVER stage0(
        .v0(v0_source), .v1(v1_source), .v2(v2_source), .op(instruction_op),
        .full_ins(.mblock_output),
        clk0);

    // STAGE1

    // TODO: Breakdown instruction_op into sub-operations

    // TODO: Ensure MBLOCK supplies expectations.
    // MBLOCK_MUX is expected to fetch MBLOCK based on v0_source and
    // instruction_op breakdowns and redirect the value into v0.

    // @stage1 posedge following should freeze.
    wire[31:0] v0;
    FETCH_AND_STORE stage1(
        .value(v0),
        .in(mblock_output),
        .clk(clk1));

    // STAGE2

    // TODO: Ensure MBLOCK supplies expectations.
    // MBLOCK_MUX is expected to fetch MBLOCK based on v0_source and
    // instruction_op breakdowns and redirect the value into v0.

    // @stage2 posedge following should freeze.
    wire[31:0] v1;
    FETCH_AND_STORE stage2(
        .value(v1),
        .in(mblock_output),
        .clk(clk2));

    // STAGE3
    // TODO: alu_op should be computed using instruction_op breakdowns.
    wire[3:0] alu_op;
    wire[31:0] v2;

    ALU alu(
        .out(v2),
        .op(alu_op),
        .in0(v0),
        .in1(v1));

    // MBLOCK input only comes from ALU output.
    assign mblock_input = v2;

    PC_NEXT pc_next(
        .program_counter_next(program_counter_next),
        .program_counter(program_counter),
        .is_powered_on(is_powered_on));

    // @stage3 posedge following should freeze.
    wire[15:0] program_counter_next;
    flipflop16 pc(
        .out(program_counter),
        .in(program_counter_next),
        .clk(clk3));




    // PROCESSOR processor(
    //     .mblock_address(mblock_address),
    //     .mblock_input(mblock_input),
    //     .mblock_selector(mblock_selector),
    //     .mblock_output(mblock_output),

    // );

endmodule