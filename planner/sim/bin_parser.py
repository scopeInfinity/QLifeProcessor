import random
import logging

from typing import List, Optional
from planner import instruction
from planner.sim import devices

PROGRAM_ORG = 0x40
IO_DEVICES = 16

def binary_array_num(arr: List[int]):
    return sum([x<<(8*i) for i, x in enumerate(arr)])

FLAGS_BIT_VW_ZERO = 0
class BinRunner:
    def __init__(self, content):
        self.ram = []
        self.input_devices = [None]*IO_DEVICES
        self.output_devices = [None]*IO_DEVICES
        for _ in range(PROGRAM_ORG):
            self.ram.append(random.randint(0, 256))

        self.parse(content)
        self.pc_next = PROGRAM_ORG
        self.pc = None
        # self.is_powered_on = False
        # self.step()
        self.is_powered_on = True
        self.flags = [0]
        # self.step()

    def set_input_device(self, index: int, d: devices.InputDevice):
        self.input_devices[index] = d

    def set_output_device(self, index: int, d: devices.Device):
        self.output_devices[index] = d

    def parse(self, content: str):
        content = content.replace(" ", "").replace("\n", "")
        assert len(content)%8 == 0
        assert set(content) <= set(['0', '1'])
        program_size = int(content[:8], 2)
        assert program_size*8+8 == len(content)
        for i in range(1, len(content)//8):
            self.ram.append(int(content[i*8:(i+1)*8], 2))

    def read_ram(self, addr: int, count: int) -> List[int]:
        ans = []
        assert addr >= 0
        for i in range(count):
            if addr+i >= len(self.ram):
                ans.append(random.randint(0, 256))
            else:
                ans.append(self.ram[addr+i])

        logging.info("RAM[%04x] => %s", addr, ans)
        return ans

    def write_ram(self, addr: int, count: int, value: int) -> List[int]:
        arr_value = []
        for i in range(count):
            arr_value.append(value&255)
            value>>=8

        assert addr >= 0
        for i in range(count):
            self.ram[(i+addr)%len(self.ram)] = arr_value[i]

        logging.info("RAM[%04x] <= %s", addr, arr_value)

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
            value = input_devices[vr_source].take_input()
            assert value >= 0 and value < (1<<32)
            return value
        raise Exception(f"unsupported selector: {sel}")


    def m_fetch_and_store_stage2(
        self,
        vr_value: int,
        vrw_source: int,
        sel: instruction.MBlockSelector_stage2):
        assert vrw_source >= 0 and vrw_source < 256
        if sel == instruction.MBlockSelector_stage2.VR_VALUE_RAM:
            return binary_array_num(self.read_ram(vr_value, 4))  # reading from 32-bit address
        if sel == instruction.MBlockSelector_stage2.VRW_SOURCE_RAM:
            return binary_array_num(self.read_ram(vrw_source, 4))  # reading from 8-bit address
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
            self.pc_next = vw_value
            return
        if sel == instruction.MBlockSelector_stage3.PC_NEXT_IF_ZERO:
            # check previous vw_value flags
            if self.flags[FLAGS_BIT_VW_ZERO] == 1:
                self.pc_next = vw_value
            return
        raise Exception(f"unsupported selector: {sel}")

    def m_alu(self, rw: int, r: int, op: instruction.ALU):
        assert rw>=0 and rw<(1<<32)
        assert r>=0 and r<(1<<32)
        MASK = ((1<<32)-1)
        if op == instruction.ALU.ADD:
            return MASK&(rw+r)
        if op == instruction.ALU.SUB:
            # TODO: deal with negative number
            return MASK&(rw-r)
        if op == instruction.ALU.SHL:
            return MASK&(rw<<r)
        if op == instruction.ALU.SHR:
            return MASK&(rw>>r)
        if op == instruction.ALU.PASS_R:
            return MASK&(r)
        if op == instruction.ALU.PASS_RW:
            return MASK&(rw)
        if op == instruction.ALU.AND:
            return MASK&(rw&r)
        if op == instruction.ALU.OR:
            return MASK&(rw|r)
        raise Exception(f"unsupported ALU op: {op}")

    @staticmethod
    def m_pc_next(pc: int, value: int, flag_alu_zero: bool, update_program_counter: bool, is_powered_on: bool):
        if not is_powered_on:
            return PROGRAM_ORG
        if update_program_counter:
            return value
        # TODO: handle JEQ
        return pc+4

    def step(self):
        self.pc = self.pc_next
        self.pc_next = self.pc + 4
        logging.info("PC: 0x%x, flags: %s", self.pc, self.flags)
        ins_binary = self.read_ram(self.pc, 4)
        ins = instruction.FullyEncodedInstruction.from_binary(ins_binary)
        logging.info("Instruction data: %s", ins)
        logging.info("Instruction encoding: %s",
            [str(x) for x in instruction.get_parsers_from_encoding(ins.encoded_instruction)])
        mblock_s1 = ins.encoded_instruction.mblock_s1
        mblock_s2 = ins.encoded_instruction.mblock_s2
        mblock_s3 = ins.encoded_instruction.mblock_s3
        alu_op = ins.encoded_instruction.alu_op

        vr_source = ins.address_r.get()
        vrw_source = ins.address_rw.get()

        vr_value = self.m_fetch_and_store_stage1(
            self.input_devices,
            vr_source,
            mblock_s1)
        vrw_value = self.m_fetch_and_store_stage2(
            vr_value,
            vrw_source,
            mblock_s2)

        vw_value = self.m_alu(vrw_value, vr_value, alu_op)

        self.m_fetch_and_store_stage3(
            self.output_devices,
            vw_value,
            vrw_value,
            vrw_source,
            mblock_s3)

        self.flags[FLAGS_BIT_VW_ZERO] = 1 if (vw_value==0) else 0

