from ram import RAM
import specs

class Components:
    def __init__(self) -> None:
        self.ram = RAM(specs.RAM_SIZE)
        pass