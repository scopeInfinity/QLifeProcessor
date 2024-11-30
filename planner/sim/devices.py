from typing import List
import logging


class Device:
    def __init__(self, bits = 8):
        assert 1 <= bits and bits <= 32
        self.value = [0 for _ in range(bits)]
        self.change_handlers = []

    def add_change_handler(self, f):
        self.change_handlers.append(f)

    def _new_value(self, val):
        if val != self.value:
            for handle in self.change_handlers:
                handle(val, self.value)
            self.value = val

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

    def take_input(self):
        # empty device
        pass


class LatchInput(InputDevice):
    def __init__(self, name: str, **kwargs):
        super(LatchInput, self).__init__(**kwargs)
        self.name = name
        self.update(0)

    def set_input(self, value: int):
        self.update(value)

    def take_input(self):
        print(f"Input for Latch[{self.name}]: ", end="")
        return self.get()


class Numpad(InputDevice):
    def __init__(self, name: str):
        bits = 10
        super(Numpad, self).__init__(bits=bits)
        self.name = name
        self.update(0)

    def take_input(self):
        print(f"Input for Numpad[{self.name}]: ", end="")
        val = int(input())
        assert val >= 0 and val <= 9
        self.flip_bit(val)
        return self.get()


class IntegerOutput(Device):
    def __init__(self, name: str):
        self.name = name
        super(IntegerOutput, self).__init__(bits=16)

        def _on_change(new_val, old_val):
            self.on_change(new_val, old_val)
        self.add_change_handler(_on_change)

    def on_change(self, new_val, old_val):
        print(f"Output [{self.name}]: {new_val}")

