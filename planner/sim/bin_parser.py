import random
import logging

from typing import List, Optional
from planner import instruction, memory, util
from planner.sim import devices

IO_DEVICES = 16

RAM_SIZE = 0x10000  # 64KB

def binary_array_num(arr: List[int]):
    return sum([x<<(8*i) for i, x in enumerate(arr)])

FLAGS_BITS = 2
FLAGS_BIT_VW_ZERO = 0
FLAGS_BIT_EXECUTE_FROM_RAM = 1

class BinRunner:
    def __init__(self, clock: devices.Clock, ram: devices.RAM, brom: devices.ROM):
        self.ram = ram
        self.brom = brom
        self.ram.is_write.update(0)

        self.input_devices = [None]*IO_DEVICES
        self.output_devices = [None]*IO_DEVICES

        # self.parse_bs(bootsequence_binary)
        self.reg_pc_next = memory.BOOTSEQUENCE_ORG
        self.pc = None
        # self.is_powered_on = False
        # self.step()
        self.is_powered_on = True
        self.flags = [0]*FLAGS_BITS
        # self.step()

        self.stage = 0
        def _on_clock_change(new_val, old_val):
            if new_val[0] == 1:
                assert old_val[0] == 0
                self.clock_up()
        clock.add_change_handler(_on_clock_change)

    def clock_up(self):
        if self.stage == 0:
            self.trigger_stage0()
        elif self.stage == 1:
            self.trigger_stage1()
        elif self.stage == 2:
            self.trigger_stage2()
        elif self.stage == 3:
            self.trigger_stage3()
        self.stage = (self.stage+1)%4

    def set_input_device(self, index: int, d: devices.InputDevice):
        self.input_devices[index] = d

    def set_output_device(self, index: int, d: devices.Device):
        self.output_devices[index] = d


    def read_ram(self, addr: int, count: int) -> List[int]:
        assert count == 4
        self.ram.address_line.update(addr)
        ins_binary = self.ram.value_out_line.get()
        ins_binary_array = util.to_little_32binaryarray(ins_binary)
        return ins_binary_array

    def write_ram(self, addr: int, count: int, value: int) -> List[int]:
        self.ram.address_line.update(addr)
        assert count == 4
        self.ram.value_in_line.update(value)
        self.ram.is_write.update(1)
        self.ram.is_write.update(0)


    def m_fetch_and_store_stage1(
        self,
        input_devices: List[devices.InputDevice],
        vr_source: int,
        sel: instruction.MBlockSelector_stage1):
        assert vr_source >= 0 and vr_source < 256
        if sel == instruction.MBlockSelector_stage1.VR_SOURCE_RAM:
            return binary_array_num(self.read_ram(vr_source, 4))  # reading from 8-bit address
        if sel == instruction.MBlockSelector_stage1.VR_SOURCE_CONST:
            # resize from 1 to 4 bytes
            return vr_source
        if sel == instruction.MBlockSelector_stage1.VR_SOURCE_IO:
            value = input_devices[vr_source].get()
            assert value >= 0 and value < (1<<32)
            return value
        raise Exception(f"unsupported selector: {sel}")


    def m_fetch_and_store_stage2(
        self,
        vr_source: int,
        vr_value: int,
        vrw_source: int,
        sel: instruction.MBlockSelector_stage2):
        assert vr_source >= 0 and vr_source < 256
        assert vrw_source >= 0 and vrw_source < 256
        if sel == instruction.MBlockSelector_stage2.VR_VALUE_RAM:
            return binary_array_num(self.read_ram(vr_value, 4))  # reading from 32-bit address
        if sel == instruction.MBlockSelector_stage2.VRW_SOURCE_RAM:
            return binary_array_num(self.read_ram(vrw_source, 4))  # reading from 8-bit address
        if sel == instruction.MBlockSelector_stage2.VRW_SOURCE_CONST:
            return vrw_source
        if sel == instruction.MBlockSelector_stage2.VR_SOURCE_SHL8_VRW_SOURCE_RAM:
            return binary_array_num(self.read_ram((vr_source<<8) | vrw_source, 4))  # reading from 16-bit address
        if sel == instruction.MBlockSelector_stage2.VR_SOURCE_SHL8_VRW_SOURCE_CONST:
            return (vr_source<<8) | vrw_source
        if sel == instruction.MBlockSelector_stage2.PC:
            return self.pc
        raise Exception(f"unsupported selector: {sel}")

    def m_fetch_and_store_stage3(
        self,
        output_devices: List[devices.Device],
        vw_value: int,
        vrw_value: int,
        vrw_source: int,
        sel: instruction.MBlockSelector_stage3):
        assert vrw_source >= 0 and vrw_source < 256
        if sel == instruction.MBlockSelector_stage3.NO_WRITE:
            return
        if sel == instruction.MBlockSelector_stage3.VRW_SOURCE_RAM:
            return self.write_ram(vrw_source, 4, vw_value)  # write using 8-bit address
        if sel == instruction.MBlockSelector_stage3.VRW_VALUE_RAM:
            return self.write_ram(vrw_value, 4, vw_value)  # write using 8-bit address
        if sel == instruction.MBlockSelector_stage3.VRW_SOURCE_IO:
            assert vw_value >= 0 and vw_value < (1<<32)
            output_devices[vrw_source].update(vw_value)
            return
        if sel == instruction.MBlockSelector_stage3.PC_NEXT:
            self.reg_pc_next = vw_value
            self.flags[FLAGS_BIT_EXECUTE_FROM_RAM] = 1
            return
        if sel == instruction.MBlockSelector_stage3.PC_NEXT_IF_ZERO:
            # check previous vw_value flags
            if self.flags[FLAGS_BIT_VW_ZERO] == 1:
                self.reg_pc_next = vw_value
            return
        if sel == instruction.MBlockSelector_stage3.PC_NEXT_IF_NOT_ZERO:
            # check previous vw_value flags
            if self.flags[FLAGS_BIT_VW_ZERO] == 0:
                self.reg_pc_next = vw_value
            return
        if sel == instruction.MBlockSelector_stage3.HLT:
            self.is_powered_on = False
            return

        raise Exception(f"unsupported selector: {sel}")

    def m_alu(self, rw: int, r: int, op: instruction.ALU):
        assert rw>=0 and rw<(1<<32)
        assert r>=0 and r<(1<<32)
        return instruction.ALU.execute(op, rw, r)

    def is_power_on(self):
        return self.is_powered_on

    def print_bootsequence_completed(self):
        if hasattr(self, "_print_bootsequence_completed"):
            return
        self._print_bootsequence_completed = True
        print("Boot sequence completed")

    def trigger_stage0(self):
        if not self.is_powered_on:
            return
        self.pc = self.reg_pc_next
        logging.debug("[stage0] PC: 0x%x, flags: %s", self.pc, self.flags)

        # Read instruction
        if self.flags[FLAGS_BIT_EXECUTE_FROM_RAM] == 0:
            brom_address = self.pc-memory.BOOTSEQUENCE_LOAD
            self.brom.address_line.update(brom_address)
            ins_binary = self.brom.value_line.get()
        else:
            self.print_bootsequence_completed()
            self.ram.address_line.update(self.pc)
            ins_binary = self.ram.value_out_line.get()
        ins_binary_array = util.to_little_32binaryarray(ins_binary)
        ins = instruction.FullyEncodedInstruction.from_binary(ins_binary_array)
        logging.debug("Instruction data: %s", ins)
        logging.debug("Instruction encoding: %s",
            [str(x) for x in instruction.get_parsers_from_encoding(ins.encoded_instruction)])

        self.reg_mblock_s1 = ins.encoded_instruction.mblock_s1
        self.reg_mblock_s2 = ins.encoded_instruction.mblock_s2
        self.reg_mblock_s3 = ins.encoded_instruction.mblock_s3
        self.reg_alu_op = ins.encoded_instruction.alu_op

        self.reg_vr_source = ins.address_r.get()
        self.reg_vrw_source = ins.address_rw.get()

    def trigger_stage1(self):
        if not self.is_powered_on:
            return
        self.reg_pc_next = self.pc + 4
        logging.debug("[stage1] reg_vr_source: 0x%x, reg_mblock_s1: %s", self.reg_vr_source, self.reg_mblock_s1)
        self.reg_vr_value = self.m_fetch_and_store_stage1(
            self.input_devices,
            self.reg_vr_source,
            self.reg_mblock_s1)


    def trigger_stage2(self):
        if not self.is_powered_on:
            return
        logging.debug("[stage2] reg_vr_source: 0x%x, "
                      "reg_vr_value: 0x%x, "
                      "reg_vrw_source: 0x%x, "
                      "reg_mblock_s2: %s, "
                      "reg_alu_op: %s",
                      self.reg_vr_source,
                      self.reg_vr_value,
                      self.reg_vrw_source,
                      self.reg_mblock_s2,
                      self.reg_alu_op)
        self.reg_vrw_value = self.m_fetch_and_store_stage2(
            self.reg_vr_source,
            self.reg_vr_value,
            self.reg_vrw_source,
            self.reg_mblock_s2)

        self.reg_vw_value = self.m_alu(
            self.reg_vrw_value,
            self.reg_vr_value,
            self.reg_alu_op)


    def trigger_stage3(self):
        if not self.is_powered_on:
            return
        logging.debug("[stage3] reg_vw_value: 0x%x, "
                      "reg_vrw_value: 0x%x, "
                      "reg_vrw_source: 0x%x, "
                      "reg_mblock_s3: %s",
                      self.reg_vw_value,
                      self.reg_vrw_value,
                      self.reg_vrw_source,
                      self.reg_mblock_s3)
        self.m_fetch_and_store_stage3(
            self.output_devices,
            self.reg_vw_value,
            self.reg_vrw_value,
            self.reg_vrw_source,
            self.reg_mblock_s3)

        # TODO: Move it to stage2
        self.flags[FLAGS_BIT_VW_ZERO] = 1 if (self.reg_vw_value==0) else 0

