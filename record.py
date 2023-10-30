import pyautogui as pg
from pynput.keyboard import Listener
from pynput import keyboard
import os
import json
import constants

def create_folder():
    if not os.path.isdir(constants.FOLDER_NAME_DUNGEON):
        os.mkdir(constants.FOLDER_NAME_DUNGEON)

class Rec:
    def __init__(self):
        self.count = 0
        create_folder()
        self.coordinates = []

    def photo(self):
        x, y = pg.position()
        photo = pg.screenshot(region=(x-3, y-3, 6, 6))
        path = f'{constants.FOLDER_NAME_DUNGEON}/flag_{self.count}.png'
        photo.save(path)
        self.count = self.count + 1
        info = {
            "path": path,
            "down": 0,
            "up": 0,
            "wait": 10
        }
        self.coordinates.append(info)

    def key_code(self, key):
       if key == keyboard.Key.esc:
            with open(f'{constants.FOLDER_NAME_DUNGEON}/info.json','w') as file:
                file.write(json.dumps(self.coordinates))
            return False
       if key == keyboard.Key.insert:
            self.photo()
       if key == keyboard.Key.page_down:
            self.down()
       if key == keyboard.Key.page_up:
            self.up()

    def down():
        last_coord = self.coordinates[-1]
        last_coord['down'] = 1

    def up():
        last_coord = self.coordinates[-1]
        last_coord['up'] = 1

    def start(self):
        with Listener(on_press=self.key_code) as listener:
            listener.join()


record = Rec()
record.start()