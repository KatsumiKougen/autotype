from pynput import mouse, keyboard
from pynput.keyboard import Key
from time import sleep
import json, sys, time

with open("debug.log", "a") as f:
    f.write(time.asctime()+"\n")

debug = True
def debugPrint(string: str, allowed: bool = debug):
    if allowed:
        with open("debug.log", "a") as f:
            f.write(string+"\n")

class tool:

    def __init__(self):
        self.kb = keyboard.Controller()
        self.special = {
            "alt": Key.alt,
            "bksp": Key.backspace,
            "ctrl": Key.ctrl,
            "cmd": Key.cmd,
            "del": Key.delete,
            "down": Key.down,
            "end": Key.end,
            "enter": Key.enter,
            "esc": Key.esc,
            "f1": Key.f1,
            "f2": Key.f2,
            "f3": Key.f3,
            "f4": Key.f4,
            "f5": Key.f5,
            "f6": Key.f6,
            "f7": Key.f7,
            "f8": Key.f8,
            "f9": Key.f9,
            "f10": Key.f10,
            "f11": Key.f11,
            "f12": Key.f12,
            "home": Key.home,
            "ins": Key.insert,
            "left": Key.left,
            "pgdn": Key.page_down,
            "pgup": Key.page_up,
            "pause": Key.pause,
            "prtsc": Key.print_screen,
            "right": Key.right,
            "shift": Key.shift,
            "tab": Key.tab,
            "up": Key.up
        }

    def loadKeyList(self, filename: str):
        try:
            debugPrint(
                f"Now loading \"{filename}\"...\n"
                f"  File name: {filename.split('.')[0]}\n"
                f"  Format: {filename.split('.')[1]}"
            )
            if filename.split(".")[-1] != "json":
                print(f"Error: Got .{filename.split('.')[-1]} file, expected .json file")
            else:
                with open(filename, "r") as f:
                    self.keylist = json.load(f)
                print(f"{filename} loaded!")
        except FileNotFoundError:
            print(f"Error: No such file as {filename}")
        except json.decoder.JSONDecodeError:
            print(f"Error: Syntax error in {filename}")

    def typeKey(self, keyName: keyboard.Key, delay: int):
        self.kb.press(keyName)
        self.kb.release(keyName)
        sleep(delay)
        debugPrint(f"Key \"{keyName}\" pressed, {delay:.2f} seconds interval")

    def holdKey(self, *keyName: keyboard.Key, delay: int):
        for key in keyName:
            self.kb.press(key)
            debugPrint(f"Key {key} held")
        for key in keyName:
            self.kb.release(key)
            debugPrint(f"Key {key} released")

    def convert(self, keyString: str) -> list:
        return [self.special[key] if key in self.special else key for key in keyString.split(".")]

    def start(self):
        sleep(5)
        defaultSpeed = 0.0384
        debugPrint(f"Interval: {defaultSpeed} seconds\nReady to type in 5 seconds...")
        for idx, item in enumerate(self.keylist):
            if item[-1] == "type":
                for char in item[0]:
                    self.typeKey(char, delay=defaultSpeed)
            elif item[-1] == "hold":
                self.holdKey(*(self.convert(item[0])), delay=defaultSpeed)
            elif item[-1] == "special":
                self.typeKey(self.special[item[0]], delay=defaultSpeed)
            debugPrint(f"Item {idx}\tContent: {item[0]}\nMode: {item[-1]}")

tool = tool()
tool.loadKeyList(sys.argv[1])
tool.start()
