import keyboard_module as kb
from djitellopy import Tello
import time

kb.init()

tello = Tello()
tello.connect()
print('Status | Battery=', tello.get_battery())

def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50

    if kb.getKey("LEFT"): lr = -speed
    elif kb.getKey("RIGHT"): lr = speed

    if kb.getKey("UP"): fb = speed
    elif kb.getKey("DOWN"): fb = -speed

    if kb.getKey("w"): ud = speed
    elif kb.getKey("s"): ud = -speed

    if kb.getKey("a"): yv = speed
    elif kb.getKey("d"): yv = -speed

    if kb.getKey("h"): tello.takeoff()
    if kb.getKey("q"): tello.land()

    return [lr, fb, ud, yv]


while True:
    vals = getKeyboardInput()
    tello.send_rc_control(vals[0],vals[1],vals[2],vals[3])
    time.sleep(0.05)