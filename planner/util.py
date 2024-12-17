import string

LABEL_CONSTANT = "constant"
LABEL_TMP = "__tmp__"

def is_valid_label(msg):
    if len(msg) == 0:
        return False
    if msg[0] in string.digits:
        return False
    if msg in [f"R{i}" for i in range(10)]:
        return False
    if msg in ["section", "data", "bss"]:
        return False
    return set(msg) <= set(string.ascii_uppercase + string.ascii_lowercase + string.digits + "_")

def to_big_32binary(val):
    return f"{val:032b}"

def to_little_32binary(val):
    big = to_big_32binary(val)
    return ''.join([big[i*8:(i+1)*8] for i in range(4)[::-1]])

def from_little_32binary(little):
    assert len(little) == 32
    return sum([int(little[i*8:(i+1)*8],2)<<(8*i) for i in range(4)])
