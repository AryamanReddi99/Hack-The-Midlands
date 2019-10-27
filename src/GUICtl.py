import pyautogui as pg
import platform
from time import sleep

def lock_screen():
    if platform.system() == "Linux":
        pg.hotkey('winleft', 'l')
    else:
        print("Not implemented for this platform")

def workspace_up():
    if platform.system() == "Linux":
        pg.press('winleft')
        sleep(0.3)
        pg.press('pageup')
        sleep(0.3)
        pg.press('winleft')
        sleep(0.3)
    else:
        print("Not implemented for this platform")

def workspace_down():
    if platform.system() == "Linux":
        pg.press('winleft')
        sleep(0.3)
        pg.press('pagedown')
        sleep(0.3)
        pg.press('winleft')
        sleep(0.3)
    else:
        print("Not implemented for this platform")

