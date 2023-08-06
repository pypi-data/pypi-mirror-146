import pynput
from datetime import datetime
from .common import Event, EventKind

class KeyboardRecorder:
    def __init__(self):
        self.recordPress = True
        self.recordRelease = True
        self.listener = None
        self.events = []

    def on_press(self, key):
        self.events.append(Event(datetime.now() - self.basetime, EventKind.KEY_PRESS, [key]))

    def on_release(self, key):
        self.events.append(Event(datetime.now() - self.basetime, EventKind.KEY_RELEASE, [key]))

    def start(self):
        self.basetime = datetime.now()
        self.listener = pynput.keyboard.Listener(
                on_press=self.on_press if self.recordPress else None,
                on_release=self.on_release if self.recordRelease else None)
        self.listener.start()

    def stop(self):
        self.listener.stop()
        self.listener = None

    def clear(self):
        self.events = []

class MouseRecorder:
    def __init__(self):
        self.recordMove = True
        self.recordClick = True
        self.recordScroll = True
        self.listener = None
        self.events = []

    def on_move(self, x, y):
        self.events.append(Event(datetime.now() - self.basetime, EventKind.MOUSE_MOVE, [x, y]))

    def on_click(self, x, y, button, pressed):
        self.events.append(Event(datetime.now() - self.basetime, EventKind.MOUSE_CLICK, [x, y, button, pressed]))

    def on_scroll(self, x, y, dx, dy):
        self.events.append(Event(datetime.now() - self.basetime, EventKind.MOUSE_SCROLL, [x, y, dx, dy]))

    def start(self):
        self.basetime = datetime.now()
        self.listener = pynput.mouse.Listener(
                on_move=self.on_move if self.recordMove else None,
                on_click=self.on_click if self.recordClick else None,
                on_scroll=self.on_scroll if self.recordScroll else None)
        self.listener.start()

    def stop(self):
        self.listener.stop()
        self.listener = None
    
    def clear(self):
        self.events = []
