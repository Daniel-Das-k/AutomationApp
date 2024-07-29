import webbrowser
import pyautogui
import time


name = input("name:")
msg = input("msg: ")
# webbrowser.open("https://web.whatsapp.com/")
time.sleep(10)
pyautogui.click(236,228)
pyautogui.typewrite(name)
time.sleep(5)
pyautogui.click(239,386)
time.sleep(5)
pyautogui.typewrite(msg)
time.sleep(10)
print(pyautogui.position())
pyautogui.click(1407,829)
