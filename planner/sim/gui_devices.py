from planner.sim import devices
import logging
import pygame

class GUIDevice:
    def __init__(self):
        self.offset_x = 0
        self.offset_y = 0

    def set_offset(self, offset: tuple[int, int]):
        self.offset_x = offset[0]
        self.offset_y = offset[1]

    def draw(self, surface):
        pass

    def draw_width(self):
        return 1

    def draw_height(self):
        return 1


class GUIDeviceManager:
    def __init__(self):
        self.devices = []
        self.padding = 10

    def add_device(self, offset: tuple[int, int], dev: GUIDevice):
        dev.set_offset((offset[0]+self.padding, offset[1]+self.padding))
        self.devices.append(dev)

    def _draw(self):
        pygame.draw.rect(self.surface, (255, 255, 255), pygame.Rect(0, 0, self.width, self.height))
        for dev in self.devices:
            dev.draw(self.surface)
        pygame.display.update()

    def draw_loop(self):
        pygame.init()
        self.width = self.padding*2 + max([d.offset_x+d.draw_width() for d in self.devices])
        self.height = self.padding*2 + max([d.offset_y+d.draw_height() for d in self.devices])
        self.surface = pygame.display.set_mode((self.width, self.height))
        while True:
            self._draw()


class GUILed(GUIDevice):
    def __init__(self, display: devices.LEDDisplay):
        super(GUILed, self).__init__()
        self.led_size = 10
        self.display = display

        _state = self.display.get_display_state()
        self.lheight = len(_state)
        self.lwidth = len(_state[0])

    def draw(self, surface):
        state = self.display.get_display_state()
        for i in range(len(state)):
            for j in range(len(state[0])):
                color = (255, 0, 0) if state[i][j] else (150, 150, 150)
                x = self.led_size*(2*j+1)
                y = self.led_size*(2*i+1)
                pygame.draw.rect(surface, color, pygame.Rect(self.offset_x + x, self.offset_y + y, self.led_size, self.led_size))

    def draw_width(self):
        return self.led_size*(2*self.lwidth)

    def draw_height(self):
        return self.led_size*(2*self.lheight)



class KeyPressedInput(GUIDevice):
    def __init__(self, input: devices.LatchInput, key_bit_mapping):
        super(KeyPressedInput, self).__init__()
        self.input = input
        self.key_bit_mapping = key_bit_mapping


    def draw(self, surface):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in self.key_bit_mapping:
                    self.input.update_bit(self.key_bit_mapping[event.key], 1)
                    logging.info("Key pressed: %s", pygame.key.name(event.key))
            if event.type == pygame.KEYUP:
                if event.key in self.key_bit_mapping:
                    self.input.update_bit(self.key_bit_mapping[event.key], 0)
                    logging.info("Key released: %s", pygame.key.name(event.key))


    def draw_width(self):
        return 0

    def draw_height(self):
        return 0

