import pyautogui as p
from time import sleep
p.move(None, 100)

p.press('winleft')
sleep(0.5)
p.press('pagedown')
sleep(0.5)
p.press('winleft')
sleep(1)
p.press('winleft')
sleep(0.5)
p.press('pageup')
sleep(0.5)
p.press('winleft')

sleep(1)

p.press('winleft')
p.typewrite("Terminal", interval=0.1)
p.press('enter')

sleep(1)
p.hotkey('winleft', 'l')
