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
