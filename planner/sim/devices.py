from planner import util
from typing import List, Optional
from threading import Thread
import time
import random
import logging

class Device:
    def __init__(self, bits = 8):
        assert 0 <= bits and bits <= 32
        self.bits = bits
        self.value = [0 for _ in range(bits)]
        self.change_handlers = []
        self._never_updated = True

    def get_bit_count(self):
        return self.bits

    def add_change_handler(self, f):
        self.change_handlers.append(f)

    def _new_value(self, val):
        if self._never_updated or val != self.value:
            old_value = self.value
            self.value = val
            self._never_updated = False
            for handle in self.change_handlers:
                handle(val, old_value)

    def get(self):
        return sum([self.value[i]<<i for i in range(len(self.value))])

    def update_list(self, value: List[int]):
        assert len(self.value) == len(value)
        self._new_value(value)

    def update(self, val: int):
        value = [1 if (val&(1<<i))>0 else 0 for i in range(len(self.value))]
        self._new_value(value)

    def update_bit(self, index: int, value: int):
        assert index >= 0 and index < len(self.value)
        assert value in [0, 1]
        new_value = self.value.copy()
        new_value[index] = value
        self._new_value(new_value)


    def flip_bit(self, index: int):
        assert index >= 0 and index < len(self.value)
        new_value = self.value.copy()
        new_value[index] ^= 1
        self._new_value(new_value)


class InputDevice(Device):
    def __init__(self, *args, **kwargs):
        super(InputDevice, self).__init__(*args, **kwargs)


class LatchInput(InputDevice):
    def __init__(self, name: str, **kwargs):
        super(LatchInput, self).__init__(**kwargs)
        self.name = name
        self.update(0)

    def set_input(self, value: int):
        self.update(value)

    def get(self):
        # print(f"Input for Latch[{self.name}]: ", end="")
        return super().get()


class Clock(InputDevice):
    def __init__(self):
        super(Clock, self).__init__(bits=1)
        self.name = "clock"
        self.update(0)
        self.thread = Thread(None, self.steps)

    def start(self):
        self.thread.start()

    def steps(self,):
        while True:
            # full speed
            self.tick()

    def tick(self):
        self.flip_bit(0)

    def get(self):
        return super().get()


class Numpad(InputDevice):
    def __init__(self, name: str):
        bits = 10
        super(Numpad, self).__init__(bits=bits)
        self.name = name
        self.update(0)

    def get(self):
        print(f"Input for Numpad[{self.name}]: ", end="")
        val = int(input())
        assert val >= 0 and val <= 9
        self.flip_bit(val)
        return super().get()


class IntegerOutput(Device):
    def __init__(self, name: str, **kwargs):
        self.name = name
        super(IntegerOutput, self).__init__(**kwargs)

        def _on_change(new_val, old_val):
            self.on_change(new_val, old_val)
        self.add_change_handler(_on_change)

    def on_change(self, new_val, old_val):
        pass

class LEDDisplay(Device):
    '''
    +----------------+
    |                |
    | .              |
    |                |
    |                |
    +----------------+

    '''
    def __init__(self, name: str, use_print: Optional[bool] = True, width_anode=16, height_cathode=8):
        # Assume cathode (+ve) is at height
        # Assume anode (-ve) is at width

        super(LEDDisplay, self).__init__(bits=0)

        self.name = name
        self.height = height_cathode
        self.width = width_anode
        assert self.width <= 32
        assert self.height <= 32
        self.leds = []
        for _ in range(self.height):
            self.leds.append([0]*self.width)
        self.anodes = [IntegerOutput("anode", bits=self.width)]
        self.cathodes = [IntegerOutput("cathode", bits=self.height)]
        self.use_print = use_print
        self.led_glow_duration = 0.05 # secs
        self.led_brightness_recompute_lag = self.led_glow_duration/4 # secs/step
        self.led_brightness_reduce_per_step = self.led_brightness_recompute_lag/self.led_glow_duration

        for i in range(len(self.cathodes)):
            def _on_change(new_val, old_val):
                self.on_change_cathode(i, new_val, old_val)
            self.cathodes[i].add_change_handler(_on_change)
        for i in range(len(self.anodes)):
            def _on_change(new_val, old_val):
                self.on_change_anode(i, new_val, old_val)
            self.anodes[i].add_change_handler(_on_change)

        self.last_display = None
        self.thread = Thread(None, self.step)
        self.thread.start()
        # we aren't gonna join


    def step(self):
        while True:
            self.recompute_brightness_step()
            self.display(only_if_changed=True)
            time.sleep(self.led_brightness_recompute_lag)

    def get_anodes(self):
        return self.anodes

    def get_cathodes(self):
        return self.cathodes

    def on_change_cathode(self, index: int, new_val: int, old_val: int):
        self.refetch_voltage()

    def on_change_anode(self, index: int, new_val: int, old_val: int):
        self.refetch_voltage()

    def output_val_to_voltage(self, index: int, val):
        return 5 if (val&(1<<index))>0 else 0

    def refetch_voltage(self):
        leds_voltage_diff = []
        for _ in range(self.height):
            leds_voltage_diff.append([0]*self.width)
        _i = 0
        for i in range(len(self.cathodes)):
            for i2 in range(self.cathodes[i].get_bit_count()):
                _j = 0
                for j in range(len(self.anodes)):
                    for j2 in range(self.anodes[j].get_bit_count()):
                        leds_voltage_diff = (
                            self.output_val_to_voltage(i2, self.cathodes[i].get()) -
                            self.output_val_to_voltage(j2, self.anodes[j].get())
                            )
                        if leds_voltage_diff > 3:
                            # start glowing
                            self.leds[_i][_j] = 1
                        _j += 1
                _i += 1

    def recompute_brightness_step(self):
        for i in range(self.height):
            for j in range(self.width):
                self.leds[i][j]=max(self.leds[i][j]-self.led_brightness_reduce_per_step, 0)

    def get_display_state(self):
        state = []
        for i in range(self.height):
            val = [x>0 for x in self.leds[i]]
            val = val[::-1]  # lsb should support right most led
            state.append(val)
        return state

    def display_as_str(self):
        state = self.get_display_state()
        dis = []
        dis.append("+%s+"'' % ('-'*3*self.width))
        for i in range(len(state)):
            val = ['#' if x else '.' for x in state[i]]
            dis.append(''.join(["|%s|" % (x) for x in val]))
        dis.append("+%s+"''  % ('-'*3*self.width))
        return '\n'.join(dis)


    def display(self, only_if_changed=True):
        new_display = self.get_display_state()
        if only_if_changed and new_display == self.last_display:
            return
        self.last_display = new_display
        if self.use_print:
            print(new_display)

RAM_SIZE = 0x10000  # 64KB

class RAM(object):
    def __init__(self):
        self.name = "RAM"
        self.size = RAM_SIZE
        self.data = []
        for _ in range(RAM_SIZE):
            self.data.append(random.randint(0, 256))
        self.address_bits = 16
        self.value_bits = 32
        self.address_line = IntegerOutput("ram_address", bits=self.address_bits)
        self.is_write = IntegerOutput("ram_is_write", bits=1)
        self.value_in_line = IntegerOutput("ram_value_in", bits=self.value_bits)
        self.value_out_line = LatchInput("ram_value_out", bits=self.value_bits)

        def _on_address_change(_, __):
            address = self.address_line.get()
            value=util.from_littlearray_32binary(self.read_ram(address, 4))
            self.value_out_line.update(value)
        self.address_line.add_change_handler(_on_address_change)

        def _on_write_change(new_val, old_val):
            if new_val[0] == 1:
                assert old_val[0] == 0
                address = self.address_line.get()
                value = self.value_in_line.get()
                self.write_ram(address, 4, value)
                self.value_out_line.update(value)
        self.is_write.add_change_handler(_on_write_change)

    def read_ram(self, addr: int, count: int) -> List[int]:
        ans = []
        assert addr >= 0
        for i in range(count):
            if addr+i >= len(self.data):
                raise ValueError(f"attempted to read outside ram: {addr+i} >= {len(self.data)}")
            else:
                ans.append(self.data[addr+i])

        logging.debug("RAM[%04x] => %s", addr, ans)
        return ans

    def write_ram(self, addr: int, count: int, value: int) -> List[int]:
        arr_value = []
        for i in range(count):
            arr_value.append(value&255)
            value>>=8

        assert addr >= 0
        for i in range(count):
            self.data[i+addr] = arr_value[i]
        logging.debug("RAM[%04x] <= %s", addr, arr_value)


class ROM(object):
    def __init__(self, name: str, content: str, **kwargs):
        self.name = name
        self.content = self.parse(content)
        self.address_bits = 16
        self.value_bits = 32
        self.address_line = IntegerOutput("address", bits=self.address_bits)
        self.value_line = LatchInput("value", bits=self.value_bits)
        def _on_change(_, __):
            address = self.address_line.get()
            value=util.from_little_32binary(self.content[address*8:address*8+32])
            logging.debug("ROM[%04x] => %s, %s", address, value, self.content[address*8:address*8+32])
            self.value_line.update(value)

        _on_change(None, None)
        self.address_line.add_change_handler(_on_change)

    def parse(self, content: str):
        content = content.replace(" ", "").replace("\n", "")
        assert len(content)%8 == 0
        assert set(content) <= set(['0', '1'])
        program_size = util.from_little_32binary(content[:32])
        assert program_size*8+32 == len(content)
        return content
