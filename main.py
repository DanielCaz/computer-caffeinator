import pyautogui as pt

pt.sleep(1)

while True:
    pt.hotkey("ctrl", "j")

    pt.sleep(0.5)

    pt.hotkey("ctrl", "n")

    pt.typewrite("Hello, World! ", interval=0.5)

    pt.sleep(15)
