import pyautogui as pg
import keyboard
import actions
import constants

def eat_food():
    pg.press('F4')
    print('Comendo')

def hole_down(should_down):
    if should_down:
        box = pg.locateOnScreen(f'{constants.FOLDER_NAME}/down_mark.png', confidence=0.8)
        if box:
            x, y = pg.center(box)
            pg.moveTo(x, y)
            pg.click()
            pg.sleep(10)

def hole_up(should_up, img, x_1, y_1):
    if should_up:
        box = pg.locateOnScreen(img, confidence=0.8)
        if box:
            x, y = pg.center(box)
            pg.moveTo(x+x_1, y+y_1)
            pg.click()
            pg.sleep(10)

def check_status(name, delay, x, y, rgb, button_name):
    print(f'check {name}')
    pg.sleep(delay)
    if pg.pixelMatchesColor(x, y, rgb):
        pg.press(button_name)

def check_battle():
    pg.locateOnScreen(f'{constants.FOLDER_NAME}/region_battle.PNG', region=constants.REGION_BATTLE)

def check_anchor():
     box = pg.locateOnScreen(f'{constants.FOLDER_NAME}/anchor.PNG', confidence=0.8)
     if box:
        pg.moveTo(1893, 12)
        pg.click()
        pg.moveTo(1893, 12)
        pg.click(1105, 550)
        return False
    return True
