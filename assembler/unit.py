from typing import List, Optional
import assembler.instruction as instruction
import asm_parser
import util


def get_operand_cm(label_or_not: str):
    assert isinstance(label_or_not, str)
    if util.is_memory_operand(label_or_not):
        return OperandM(Label(label_or_not[1:-1]))
    else:
        return OperandC(Label(label_or_not))

class Label:
    def __init__(self, label_or_val: str) -> None:
        if util.is_valid_label(label_or_val):
            self.label = label_or_val
            self.value = None
        else:
            self.label = None
            self.value = int(label_or_val, 0)

    def resolve_it(self):
        if self.label is not None and self.value is None:
            self.value = asm_parser.AsmParser.get_instance().get_label_value(self.label)

    def get_str(self, resolved=False, binary=False):
        if resolved:
            self.resolve_it()

        if binary:
            assert resolved
            assert self.value is not None
            return f"{self.value:08b}"

        if resolved or self.label is None:
            return f"0x{self.value:x}"
        else:
            return self.label

class Operand:
    pass

class OperandC(Operand):
    def __init__(self, val: Label) -> None:
        super().__init__()
        self.val = val

    def get_str(self, resolved=False, binary=False):
        return self.val.get_str(resolved=resolved, binary=binary)

class OperandM(Operand):
    def __init__(self, address: Label) -> None:
        super().__init__()
        self.address = address

    def get_str(self, resolved=False, binary=False):
        if binary:
            return self.address.get_str(resolved=resolved, binary=binary)
        return f"[{self.address.get_str(resolved=resolved)}]"


class Instruction:
    def __init__(self, ins, *operands: List[Operand]) -> None:
        self.ins = ins
        self.operands = operands

    def size(self):
        return 4

    def get_str(self, resolved=False, binary=False):
        if not binary:
            return f"{self.ins}  {','.join([o.get_str(resolved=resolved) for o in self.operands])}"
        assert resolved
        do_not_care = "00000000"
        # binary representation
        out0 = f"{instruction.ENCODING[self.ins]:08b}"
        # TODO: needs works, as this represents fake representation
        out1 = do_not_care
        if len(self.operands) > 0:
            out1 = self.operands[0].get_str(resolved=True, binary=True)
        out2 = do_not_care
        if len(self.operands) > 1:
            out2 = self.operands[1].get_str(resolved=True, binary=True)
        out3 = do_not_care
        return out0 + out1 + out2 + out3


class Data:
    def __init__(self, byte: Optional[int]):
        self.byte=byte

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