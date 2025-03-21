from typing import List, Optional
from planner import util
from enum import Enum
import logging


class LazyLabel:
    def __init__(self, name: str, value: Optional[int] = None, override_get = None):
        assert util.is_valid_label(name), ValueError(f"{name} is not a valid label")
        self.name = name
        if name == util.LABEL_CONSTANT:
            assert value is not None
        self.value = value
        self.override_get = override_get

    def __repr__(self):
        if self.name == util.LABEL_CONSTANT:
            return str(self.value)
        return self.name

    def __eq__(self, o):
        if isinstance(o, int):
            return self.value == o
        if isinstance(o, LazyLabel):
            if self.name == util.LABEL_CONSTANT:
                return self.value == o.value
            return self.name == o.name
        return False

    def shr(self, shift):
        def new_get(ensure_resolved=False):
            if not ensure_resolved:
                return 0
            return self.get(ensure_resolved)>>shift
        return LazyLabel(util.LABEL_TMP, override_get=new_get)

    def add(self, val):
        def new_get(ensure_resolved=False):
            if not ensure_resolved:
                return 0
            return self.get(ensure_resolved)+val
        return LazyLabel(util.LABEL_TMP, override_get=new_get)

    def bin_and(self, val):
        def new_get(ensure_resolved=False):
            if not ensure_resolved:
                return 0
            return self.get(ensure_resolved)&val
        return LazyLabel(util.LABEL_TMP, override_get=new_get)

    def get(self, ensure_resolved=False):
        if self.override_get is not None:
            return self.override_get(ensure_resolved=ensure_resolved)
        if ensure_resolved:
            assert self.value is not None
            return self.value
        if self.value is None:
            logging.info("LazyLabel[%s] is empty", self.name)
            return 0
        return self.value

    def assign(self, o):
        if not isinstance(o.value, int):
            raise ValueError(f"{self.name} resolution failed during assign as {o.value}")
        if self.value is None:
            self.value = o.value
        else:
            assert self.value == o.value

    def get_str(self, resolved=False):
        if self.name == util.LABEL_CONSTANT:
            return str(self.value)
        if not resolved:
            return self.name
        value = self.get(ensure_resolved=True)
        return str(value)


class Operand(Enum):
    ADDRESS = 1
    CONSTANT = 2
    # Address of address, equivalent of pointers
    DADDRESS = 3

    def __repr__(self):
        return self.name


class Data:
    def __init__(self, byte: Optional[int] = None):
        self.byte=byte
        if self.byte is not None:
            if self.byte >= 256:
                raise ValueError(f"data is more than a byte: {byte}")

    def size(self):
        return 1

    def get_str(self, resolved=False, binary=False):
        if binary:
            if self.byte is None:
                return "--------"
            return f"{self.byte:08b}"
        else:
            if self.byte is None:
                return "--"
            return f"{self.byte:02}"

    def __repr__(self) -> str:
        return self.get_str(binary=True)
