from modules.tests import keyboard_module as kb
from djitellopy import Tello
import time,cv2

kb.init()

tello = Tello()
tello.connect()
print('Status | Battery=', tello.get_battery())

global img

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

    if kb.getKey("h"): 
        tello.takeoff()
        time.sleep(3)

    if kb.getKey("q"): 
        tello.send_rc_control(0,0,0,0)
        tello.land()
        print(tello.get_distance_tof())

    if kb.getKey("t"):
        cv2.imwrite(f'resources/images/{time.time()}.jpg', img)
        time.sleep(0.3)

    return [lr, fb, ud, yv]

tello.streamon() # EDU no support when connected to wifi

while True:
    vals = getKeyboardInput()
    tello.send_rc_control(vals[0],vals[1],vals[2],vals[3])
    
    # print('Status | TOF=', tello.get_distance_tof())
    # print('Status | Height=', tello.get_height())

    img = tello.get_frame_read().frame
    img = cv2.resize(img, (1024, 1024))
    cv2.imshow("Image", img)
    cv2.waitKey(1)

    time.sleep(0.03)