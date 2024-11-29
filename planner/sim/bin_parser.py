import random
import logging

from typing import List, Optional
from planner import instruction
from planner.sim import devices

PROGRAM_ORG = 0x40
IO_DEVICES = 16

class BinRunner:
    def __init__(self, content):
        self.ram = []
        self.input_devices = [None]*IO_DEVICES
        self.output_devices = [None]*IO_DEVICES
        for _ in range(PROGRAM_ORG):
            self.ram.append(random.randint(0, 256))

        self.parse(content)
        self.pc = PROGRAM_ORG
        # self.is_powered_on = False
        # self.step()
        self.is_powered_on = True
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

        logging.info("RAM[%04x]: %s", addr, ans)
        return ans

    @staticmethod
    def m_fetch_and_store(
        ram: List[int],
        input_devices: List[int],
        output_devices: List[int],
        source: int,
        sel: instruction.MBlockSelector,
        mblock_is_write: bool,
        value: Optional[int] = None,
        to_be_ignored_sim_hack: Optional[bool] = False):
        if not mblock_is_write:
            if sel == instruction.MBlockSelector.RAM:
                assert source >= 0 and source < len(ram)
                return ram[source]
            if sel == instruction.MBlockSelector.CONST:
                assert source >= 0 and source < 256
                return source
            if sel == instruction.MBlockSelector.IO:
                # assert source >= 0 and source < 16
                if to_be_ignored_sim_hack:
                    value = 0
                else:
                    # print(f"Input for device[{source}]: ", end="")
                    value = input_devices[source].take_input()
                    # value = int(input(), 0)
                assert value >= 0 and value < (1<<32)
                return value
                # input_devices[source] = value
                # return input_devices[source]
        else:
            if sel == instruction.MBlockSelector.RAM:
                assert source >= 0 and source < len(ram)
                assert value >= 0 and value < 256
                ram[source] = value
                return None
            if sel == instruction.MBlockSelector.CONST:
                # no-op
                return
            if sel == instruction.MBlockSelector.IO:
                # assert source >= 0 and source < 16
                assert value >= 0 and value < (1<<32)
                # input_devices[source] = value
                output_devices[source].update(value)
                return
        raise Exception(f"unsupported selector: {sel}")

    @staticmethod
    def m_alu(rw: int, r: int, op: instruction.ALU):
        assert rw>=0 and rw<256
        assert r>=0 and r<256
        MASK = 255
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
        ins_binary = self.read_ram(self.pc, 4)
        ins = instruction.FullyEncodedInstruction.from_binary(ins_binary)
        mblock_selector_r = ins.encoded_instruction.mblock_selector_r
        mblock_selector_rw = ins.encoded_instruction.mblock_selector_rw
        alu_op = ins.encoded_instruction.alu_op
        mblock_is_write = ins.encoded_instruction.mblock_is_write
        update_program_counter = ins.encoded_instruction.update_program_counter

        vr_source = ins.address_r.get()
        vrw_source = ins.address_rw.get()

        value_r = self.m_fetch_and_store(
            self.ram,
            self.input_devices,
            self.output_devices,
            vr_source,
            mblock_selector_r,
            False,
            value=None
            )
        value_rw = self.m_fetch_and_store(
            self.ram,
            self.input_devices,
            self.output_devices,
            vrw_source,
            mblock_selector_rw,
            False,
            value=None,
            to_be_ignored_sim_hack = (alu_op == instruction.ALU.PASS_R)
            )

        value = self.m_alu(value_rw, value_r, alu_op)
        flag_alu_zero = (value == 0)

        self.m_fetch_and_store(
            self.ram,
            self.input_devices,
            self.output_devices,
            vrw_source,
            mblock_selector_rw,
            mblock_is_write and self.is_powered_on,
            value=value
            )

        self.pc = self.m_pc_next(
            self.pc,
            value,
            flag_alu_zero,
            update_program_counter,
            self.is_powered_on)
