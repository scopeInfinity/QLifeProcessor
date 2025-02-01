from planner.sim import devices
import threading

IO_DEVICES = 8
INPUT_FILE = "/tmp/ourpc_input"

global_io = None

def io_loop():
    while True:
        s = input()
        print(s)
        s=s.split()
        if s[0]=="IPC":
            pid,value = s[1], s[2]
            pid=int(pid, 16)
            value=int(value, 16)
            print("Got PID(%d) Value(%d)" % (pid, value))
            dev =  global_io.output_devices[pid]
            if dev is None:
                print("Device is None")
            else:
                dev.update(value)

class VerilogIO:
    def __init__(self):
        self.input_devices = [None]*IO_DEVICES
        self.output_devices = [None]*IO_DEVICES

        global global_io
        global_io = self
        self.mu = threading.Lock()
        self.t = threading.Thread(target=io_loop, args=[])


    def run(self, blocking=True):
        self.write_input(0, 0)
        self.t.start()
        if blocking:
            self.t.join()

    def write_input(self, new_val, old_val):
        data = [0 if i is None else i.get() for i in self.input_devices]
        data_str = '\n'.join([
          "{:032b}".format(x) for x in data
        ])
        with self.mu:
            with open(INPUT_FILE, "w") as f:
                f.write(data_str)


    def set_input_device(self, index: int, d: devices.InputDevice):
        d.add_change_handler(self.write_input)
        self.input_devices[index] = d

    def set_output_device(self, index: int, d: devices.Device):
        self.output_devices[index] = d
