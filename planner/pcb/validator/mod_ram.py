from planner.pcb.validator import rasp


# From module prespective
PIN_ADDRESS_IN = list(range(2,10))
PIN_VALUE_IN = list(range(10,18))
PIN_VALUE_OUT = list(range(18,26))
PIN_IS_WRITE = 26
PIN_CLK = 27


class ModRamValidator:
    '''Validate RAM sub-module.

    RAM sub-module is equally divided
    - At 1/4 at value line.
    - At 1/2 at address line.

    RAM module will export
     - Input: 2*8 bits address line
     - Input: 4*8 bits value line
     - Output: 32 bits value line
     - Input: 1 bit is_write
     - Input: 1 bit clk
    '''
    def __init__(self, r: rasp.PiController):
        self.r = r

    def setup(self):
        # from validator prespective
        address_out = [self.r.assign_out(p) for p in PIN_ADDRESS_IN]
        value_out = [self.r.assign_out(p) for p in PIN_VALUE_IN]
        value_in = [self.r.assign_in(p) for p in PIN_VALUE_OUT]
        is_write_out = self.r.assign_out(PIN_IS_WRITE)
        is_clk = self.r.assign_out(PIN_CLK)

    def execute_write(self, address: int, value: int):
        assert address >= 0 and address < (1<<8)
        assert value >=0 and value < (1<<8)




