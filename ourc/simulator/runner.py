from build import circuit_pb2
from pynput import keyboard
import termcolor
import time
import itertools

_LedColorToTermColor = {
    circuit_pb2.Led.RED: "on_red",
    circuit_pb2.Led.YELLOW: "on_yellow",
    circuit_pb2.Led.GREEN: "on_green",
}

def assign_or_raise_voltage(terminal_id, current_v, neigh_v):
    if current_v is None:
        return neigh_v
    if neigh_v is None:
        return current_v
    assert current_v == neigh_v, f"current_v:{current_v}, neigh_v:{neigh_v}. fault at terminal '{terminal_id}'"
    return current_v

class Sim:
    def __init__(self, circuit: circuit_pb2.Circuit):
        self.circuit = circuit
        print(self.circuit)
        self.buttons_ispressed = [False] * len(self.circuit.buttons)
        self.leds_on = [False] * len(self.circuit.leds)

        # Voltages: True (High), False (Low), None (disconnected)
        self.terminals = self.get_terminal_voltages()
        self.prep_button_handler()

    def get_terminal_voltages(self, default=False):
        ids = {}
        for b in self.circuit.buttons:
            id = b.point_a.id
            if len(id) > 0:
                ids[id] = default
            id = b.point_b.id
            if len(id) > 0:
                ids[id] = default
        for l in self.circuit.leds:
            id = l.point_anode.id
            if len(id) > 0:
                ids[id] = default
            id = l.point_cathode.id
            if len(id) > 0:
                ids[id] = default
        for v in self.circuit.voltage_sources:
            id = v.point.id
            if len(id) > 0:
                ids[id] = default
        for w in self.circuit.wires:
            for t in w.terminals:
                id = t.id
                if len(id) > 0:
                    ids[id] = default
        return ids

    def prep_button_handler(self):
        allowed_keys = {f"'{str(i)}'":i for i in range(len(self.buttons_ispressed))}
        def on_press(key):
            key = str(key)
            if key in allowed_keys:
                self.buttons_ispressed[allowed_keys[key]] = True

        def on_release(key):
            key = str(key)
            if key in allowed_keys:
                self.buttons_ispressed[allowed_keys[key]] = False

        self.key_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        self.key_listener.start()

    def update_terminal(self, t_id, voltage):
        '''Returns true if change in voltage.'''
        assert t_id in self.terminals
        if self.terminals[t_id] == voltage:
            return False
        self.terminals[t_id] = voltage
        return True

    def _process_reset_voltages(self):
        for t in self.terminals:
            self.update_terminal(t, None) # disconnected
        for vs in self.circuit.voltage_sources:
            id = vs.point.id
            if vs.voltage == circuit_pb2.VoltageSource.HIGH and len(id) > 0:
                self.update_terminal(id, True)
            elif vs.voltage == circuit_pb2.VoltageSource.LOW and len(id) > 0:
                self.update_terminal(id, False)

    def _process_propogate_voltage_terminals(self, terminal_ids):
        '''Returns True if any change in voltages.'''
        any_changes = False
        current_v = None
        # looping twice is intentional it as it will propogate
        # voltage backwards (in cycle)
        for id in itertools.chain(terminal_ids, terminal_ids):
            if len(id) == 0:
                pass # skip bad terminals
            current_v = assign_or_raise_voltage(id, current_v, self.terminals[id])
            if self.update_terminal(id, current_v):
                any_changes = True
        return any_changes


    def _process_propogate_voltage(self):
        '''Returns True if any change in voltages.'''
        any_changes = False
        for wire_no, wire in enumerate(self.circuit.wires):
            current_v = None
            ids = [t.id for t in wire.terminals]
            if self._process_propogate_voltage_terminals(ids):
                any_changes = True

        for i, pressed in enumerate(self.buttons_ispressed):
            if pressed:
                id_a = self.circuit.buttons[i].point_a.id
                id_b = self.circuit.buttons[i].point_b.id
                if self._process_propogate_voltage_terminals([id_a, id_b]):
                    any_changes = True

        # following won't work on different circuit
        for i in range(len(self.leds_on)):
            id_anode = self.circuit.leds[i].point_anode.id
            id_cathode = self.circuit.leds[i].point_cathode.id
            # current flows in one direction
            led_state = False
            if self.terminals[id_anode] == True and self.terminals[id_cathode] == False:
                led_state = True
            if self.terminals[id_anode] == False and self.terminals[id_cathode] == True:
                raise RuntimeError(f"led[{i}] exploded!")
            # if (self.terminals[id_anode] is None) or (self.terminals[id_cathode] is None):
            # not passing current if voltage isn't defined already
            # led's connected in series won't glow and will break the circuit.

            if led_state != self.leds_on[i]:
                self.leds_on[i] = led_state
                any_changes = True

        return any_changes

    def process(self):
        self._process_reset_voltages()
        changes_count = 0
        while True:
            if not self._process_propogate_voltage():
                break
            changes_count += 1
            assert changes_count < 10000, "stuck or circuit too big"

    def step(self):
        for i in range(1000):
            self.process()
        self.draw()
        time.sleep(0.1)

    def draw(self):
        print("\x1b[2J") # clear screen
        print("# Button(s)")
        for index, b in enumerate(self.circuit.buttons):
            label = f"{b.label:^10s}"
            if self.buttons_ispressed[index]:
                label = termcolor.colored(label, "black", "on_light_grey")
            print(f"[{label}] => Press Num {index}")
        print()
        print()
        print()
        print("# Led(s)")
        for index, led in enumerate(self.circuit.leds):
            label = "  "
            if self.leds_on[index]:
                label = termcolor.colored(label, None, _LedColorToTermColor.get(led.color, None))
            print(f"[{label}]")
        print()
        print()
        print()
        print("Terminal Voltage (debug)")
        for i, terminal in enumerate(self.terminals):
            print(f"{terminal}: {self.terminals[terminal]}", end="\n" if i%5 == 4 else "\t")
        print()

    def run(self):
        while(True):
            self.step()
