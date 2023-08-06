import pynput
from datetime import datetime
from .common import Event, EventKind

class Repeater:
    def __init__(self):
        self.keyboard = pynput.keyboard.Controller()
        self.mouse = pynput.mouse.Controller()

    def repeatEvents(self, events, normalize=False):
        if events == []:
            return
        events = sorted(events, key=lambda event: event.time)
        if normalize:
            for event in events:
                event.normalize(events[0].time)
        t0 = datetime.now()
        while events != []:
            if datetime.now() - t0 >= events[0].time:
                event = events.pop(0)
                if event.kind == EventKind.KEY_PRESS:
                    key = event.data[0]
                    self.keyboard.press(key)
                elif event.kind == EventKind.KEY_RELEASE:
                    key = event.data[0]
                    self.keyboard.release(key)
                elif event.kind == EventKind.MOUSE_MOVE:
                    x, y = event.data
                    self.mouse.position = (x, y)
                elif event.kind == EventKind.MOUSE_CLICK:
                    x, y, button, pressed = event.data
                    self.mouse.position = (x, y)
                    if pressed:
                        self.mouse.press(button)
                    else:
                        self.mouse.release(button)
                elif event.kind == EventKind.MOUSE_SCROLL:
                    x, y, dx, dy = event.data
                    self.mouse.position = (x, y)
                    self.mouse.scroll(dx, dy)
