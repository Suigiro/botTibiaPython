import pyautogui as pg
from pynput.keyboard import Listener
from pynput import keyboard
import actions
import constants
import threading
import myThread

def kill_monster():
    while actions.check_battle() == None:
        if event_th.is_set():
            return
        pg.press('space')
        while pg.locateOnScreen(f'{constants.FOLDER_NAME}/red_target', confidence=0.7, region=constants.REGION_BATTLE) != None:
            if event_th.is_set():
                return
            print('Monstro vivo')
        print('Aguardando novo Inimigo')

def getLoot():
    loot = pg.locateAllOnScreen(f'{constants.FOLDER_NAME}/monster_body', confidence=0.8, region=constants.REGION_LOOT)
    for box in loot:
        if event_th.is_set():
            return
        x, y = pg.center(box)
        pg.moveTo(x, y)
        pg.click(button="right")

def go_to_flag(path, wait):
    flag = pg.locateOnScreen(path, confidence=0.8, region=constants.REGION_MAP)
    if flag:
        x, y = pg.center(flag)
        if event_th.is_set():
            return
        pg.moveTo(x, y)
        pg.click()
        pg.sleep(wait)

def check_player_pos():
    box = pg.locateOnScreen(f'{constants.FOLDER_NAME}/player_point.png', confidence=0.8, region=constants.REGION_MAP)
    return box

def run():
    event_th.is_set()
    with open(f'{constants.FOLDER_NAME_DUNGEON}') as file:
        data = json.loads(file.read())
    for item in data:
        if not actions.check_anchor():
            if event_th.is_set():
                return
            kill_monster()
            if event_th.is_set():
                return
            getLoot()
            go_to_flag(item['path'], item['wait'])
            if event_th.is_set():
                return
            if check_player_pos():
                kill_monster()
                if event_th.is_set():
                    return
                pg.sleep(1)
                getLoot()
                if event_th.is_set():
                    return
                go_to_flag(item['path'], item['wait'])
            actions.eat_food()
            actions.hole_down(item['down'])
            actions.hole_up(item['up'],f'{constants.FOLDER_NAME}/up_mark_1.png', 430, 0)
            actions.hole_up(item['up'],f'{constants.FOLDER_NAME}/up_mark_2.png', 130, 130)

def key_code(key, th_group):
    if key == keyboard.Key.esc:
        event_th.set
        return False
    if key == keyboard.Key.delete:
        th_group.start()
        th_run.start()

global event_th
event_th = threading.Event()
th_run threading.Tread(target=run)

th_full_mana = myThread.myThread(lambda: actions.check_status('mana', 5, *constants.POSITION_MANA_FULL, constants.MANA_COLOR, constants.MANAATT))
th_full_life = myThread.myThread(lambda: actions.check_status('life', 5, *constants.POSITION_LIFE, constants.GREEN_LIFE, constants.LIFEREGEN))

group_thread = myThread.TreadGroup([th_full_mana, th_full_life])


 with Listener(on_press=lambda key: key_code(key, group_thread)) as listener:
    listener.join()