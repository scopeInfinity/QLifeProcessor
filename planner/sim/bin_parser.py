import random
import logging

from typing import List, Optional
from planner import instruction, memory
from planner.sim import devices

PROGRAM_ORG = memory.DEFAULT_PROGRAM_ORG
IO_DEVICES = 16

RAM_SIZE = 0x10000  # 64KB

def binary_array_num(arr: List[int]):
    return sum([x<<(8*i) for i, x in enumerate(arr)])

FLAGS_BIT_VW_ZERO = 0
class BinRunner:
    def __init__(self, content):
        self.ram = []
        self.input_devices = [None]*IO_DEVICES
        self.output_devices = [None]*IO_DEVICES
        for _ in range(RAM_SIZE):
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
        program_size = int(content[:32], 2)
        assert program_size*8+32 == len(content)
        address = PROGRAM_ORG
        for i in range(4, len(content)//8):
            self.ram[address] = (int(content[i*8:(i+1)*8], 2))
            address += 1

    def read_ram(self, addr: int, count: int) -> List[int]:
        ans = []
        assert addr >= 0
        for i in range(count):
            if addr+i >= len(self.ram):
                ans.append(random.randint(0, 256))
            else:
                ans.append(self.ram[addr+i])

        logging.debug("RAM[%04x] => %s", addr, ans)
        return ans

    def write_ram(self, addr: int, count: int, value: int) -> List[int]:
        arr_value = []
        for i in range(count):
            arr_value.append(value&255)
            value>>=8

        assert addr >= 0
        for i in range(count):
            self.ram[(i+addr)%len(self.ram)] = arr_value[i]

        logging.debug("RAM[%04x] <= %s", addr, arr_value)

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
            self.pc_next = vw_value
            return
        if sel == instruction.MBlockSelector_stage3.PC_NEXT_IF_ZERO:
            # check previous vw_value flags
            if self.flags[FLAGS_BIT_VW_ZERO] == 1:
                self.pc_next = vw_value
            return
        if sel == instruction.MBlockSelector_stage3.PC_NEXT_IF_NOT_ZERO:
            # check previous vw_value flags
            if self.flags[FLAGS_BIT_VW_ZERO] == 0:
                self.pc_next = vw_value
            return
        if sel == instruction.MBlockSelector_stage3.HLT:
            self.is_powered_on = False
            return
        raise Exception(f"unsupported selector: {sel}")

    def m_alu(self, rw: int, r: int, op: instruction.ALU):
        assert rw>=0 and rw<(1<<32)
        assert r>=0 and r<(1<<32)
        return instruction.ALU.execute(op, rw, r)

    def run_until_hlt(self):
        while self.is_powered_on:
            self.step()

    def step(self):
        if not self.is_powered_on:
            return
        self.pc = self.pc_next
        self.pc_next = self.pc + 4
        logging.debug("PC: 0x%x, flags: %s", self.pc, self.flags)
        ins_binary = self.read_ram(self.pc, 4)
        ins = instruction.FullyEncodedInstruction.from_binary(ins_binary)
        logging.debug("Instruction data: %s", ins)
        logging.debug("Instruction encoding: %s",
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
            vr_source,
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

