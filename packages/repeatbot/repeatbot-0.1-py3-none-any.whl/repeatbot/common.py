import csv
from datetime import timedelta
from enum import Enum
from pynput.keyboard import Key, KeyCode
from pynput.mouse import Button

class EventKind(Enum):
    KEY_PRESS = 0
    KEY_RELEASE = 1
    MOUSE_MOVE = 2
    MOUSE_CLICK = 3
    MOUSE_SCROLL = 4

class KeyParamType(Enum):
    KEY = 0
    KEYCODE_CHAR = 1
    KEYCODE_VK = 2

class Event:
    def __init__(self, time, kind, data):
        self.time = time
        self.kind = kind
        self.data = data

    def normalize(self, t0):
        self.time = self.time - t0

    def asCsvRow(self):
        row = [self.time.total_seconds(), self.kind.name]
        for d in self.data:
            if type(d) is Key:
                row.append(KeyParamType.KEY.name)
                row.append(d.name)
            elif type(d) is KeyCode:
                if d.char is not None:
                    row.append(KeyParamType.KEYCODE_CHAR.name)
                    row.append(d.char)
                elif d.vk is not None:
                    row.append(KeyParamType.KEYCODE_VK.name)
                    row.append(d.vk)
            elif type(d) is Button:
                row.append(d.name)
            else:
                row.append(d)
        return row
    
    @staticmethod
    def fromCsvRow(row):
        time = timedelta(seconds=float(row[0]))
        kind = EventKind[row[1]]
        if kind in [EventKind.KEY_PRESS, EventKind.KEY_RELEASE]:
            paramType, param = KeyParamType[row[2]], row[3]
            if paramType == KeyParamType.KEY:
                data = [Key[param]]
            elif paramType == KeyParamType.KEYCODE_CHAR:
                data = [KeyCode.from_char(param)]
            elif paramType == KeyParamType.KEYCODE_VK:
                data = [KeyCode.from_vk(int(param))]
        elif kind == EventKind.MOUSE_MOVE:
            x, y = int(row[2]), int(row[3])
            data = [x, y]
        elif kind == EventKind.MOUSE_CLICK:
            x, y, button, pressed = int(row[2]), int(row[3]), Button[row[4]], row[5] == "True"
            data = [x, y, button, pressed]
        elif kind == EventKind.MOUSE_SCROLL:
            x, y, dx, dy = int(row[2]), int(row[3]), int(row[4]), int(row[5])
            data = [x, y, dx, dy]
        return Event(time, kind, data)

class EventsExporter:
    @staticmethod
    def exportEvents(events, filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for event in events:
                writer.writerow(event.asCsvRow())

class EventsImporter:
    @staticmethod
    def importEvents(filename):
        events = []
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                e = Event.fromCsvRow(row)
                events.append(e)
        return events
