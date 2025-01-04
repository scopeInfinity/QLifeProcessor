// module MBLOCK_MUX(output[31:0] mblock_address,
//             output[1:0] mblock_selector,

//             input execute_from_brom,
//             input[0:3] is_stage,
//             input[15:0] address0,  // program_counter
//             input[15:0] address1,  // v0_source
//             input[15:0] address2,  // v1_source
//             input[15:0] address3,  // v2_source
//             input[3:0] is_write,
//             );

//     // TODO Starts
//     // TODO: We should support I/O and const in mblock_selector
//     // during stage0, before stage0 posedge
//     //   mblock_selector[0] = execute_from_brom;
//     //   mblock_selector[1] = 0;
//     // after stage0 posedge
//     //   mblock_selector = will come from instruction_op
//     // after stage1 posedge
//     //   mblock_selector = will come from instruction_op
//     // after stage2 posedge
//     //   mblock_selector = will come from instruction_op
//     // Challenge: How will we will fit, 3 mux_selector, ALU_OP and
//     //   instructions classes all within 1 byte...
//     // TODO Ends

//     always @(is_stage, is_write, address0, address1, address2, address3)
//     begin
//         if (is_stage == 2'b00)
//             begin
//                 // Active RAM or BROM based upon $execute_from_brom.
//                 assign mblock_selector[1:0] = {0, execute_from_brom};
//             end
//         else if (is_stage == 2'b01)
//             begin
//                 // TODO: mblock_selector compute from instruction_op
//             end
//         else if (is_stage == 2'b10)
//             begin
//                 // TODO: mblock_selector compute from instruction_op
//             end
//         else
//             begin
//                 // TODO: mblock_selector compute from instruction_op
//             end
//         else

//     end

//     MUX_8_2 m0(.value(mblock_address[ 7: 0]), .A(address0[ 7: 0]), .B(address1[ 7: 0]), ,C(address2[ 7: 0]), .D(address3[ 7: 0]), .S(mblock_selector[1:0]));
//     MUX_8_2 m1(.value(mblock_address[15: 8]), .A(address0[15: 8]), .B(address1[15: 8]), ,C(address2[15: 8]), .D(address3[15: 8]), .S(mblock_selector[1:0]));
//     MUX_8_2 m2(.value(mblock_address[23:16]), .A(address0[23:16]), .B(address1[23:16]), ,C(address2[23:16]), .D(address3[23:16]), .S(mblock_selector[1:0]));
//     MUX_8_2 m3(.value(mblock_address[31:24]), .A(address0[31:24]), .B(address1[31:24]), ,C(address2[31:24]), .D(address3[31:24]), .S(mblock_selector[1:0]));

// endmodule
