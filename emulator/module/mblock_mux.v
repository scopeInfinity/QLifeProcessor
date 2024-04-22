module MBLOCK_MUX(output[31:0] mblock_address,
            output[1:0] mblock_selector,
            input[15:0] address0,
            input[15:0] address1,
            input[15:0] address2,
            input[15:0] address3,

            input is_write0,
            input is_write1,
            input is_write2,
            input is_write3,
            );

    // TODO Starts
    // TODO: We should support I/O and const in mblock_selector
    // during stage0, before stage0 posedge
    //   mblock_selector[0] = execute_from_brom;
    //   mblock_selector[1] = 0;
    // after stage0 posedge
    //   mblock_selector = will come from instruction_op
    // after stage1 posedge
    //   mblock_selector = will come from instruction_op
    // after stage2 posedge
    //   mblock_selector = will come from instruction_op
    // Challenge: How will we will fit, 3 mux_selector, ALU_OP and
    //   instructions classes all within 1 byte...
    // TODO Ends

endmodule;