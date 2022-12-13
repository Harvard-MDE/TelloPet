from modules import keyboard_module as kb
from djitellopy import Tello
import numpy as np
import time,cv2,math



######### Params
fspeed = 120/10 # Forward speed cm/s
aSpeed = 360/6 # Angular Speed Degrees/s
interval = 0.25
dInterval = fspeed*interval
aInterval = aSpeed*interval
x,y=500,500
a = 0
yaw = 0
points = [(0,0),(0,0)]
###########################

kb.init()

tello = Tello()
tello.connect()
print('Status | Battery=', tello.get_battery())

global img

def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 15
    aspeed = 50
    global x,y,yaw,a 
    d = 0

    if kb.getKey("LEFT"): 
        lr = -speed
        d = dInterval
        a = -180

    elif kb.getKey("RIGHT"): 
        lr = speed
        d = -dInterval
        a = 180

    if kb.getKey("UP"): 
        fb = speed
        d = dInterval
        a = 270

    elif kb.getKey("DOWN"): 
        fb = -speed
        d = -dInterval
        a = -90

    if kb.getKey("w"): 
        ud = speed
    elif kb.getKey("s"): 
        ud = -speed

    if kb.getKey("a"): 
        yv = -aspeed
        yaw -= aInterval

    elif kb.getKey("d"): 
        yv = aspeed
        yaw += aInterval

    if kb.getKey("h"): 
        tello.takeoff()
        time.sleep(2)

    if kb.getKey("q"): 
        tello.send_rc_control(0,0,0,0)
        tello.land()

    if kb.getKey("t"):
        cv2.imwrite(f'resources/images/{time.time()}.jpg', img)
        time.sleep(0.3)

    time.sleep(0.25)
    a += yaw
    x += int(d*math.cos(math.radians(a)))
    y += int(d*math.sin(math.radians(a)))

    return [lr, fb, ud, yv, x, y]

tello.streamon() # EDU no support when connected to wifi

def drawPoints(img, points):
    for point in points:
        cv2.circle(img,point,5,(0,0,255),cv2.FILLED)
    cv2.circle(img,points[-1],8,(0,255,0),cv2.FILLED)
    cv2.putText(img, f'({(points[-1][0]-500)/100},{(points[-1][1]-500)/100})m',
    (points[-1][0]+10,points[-1][1]+30),cv2.FONT_HERSHEY_PLAIN, 1, (255,0,255), 1)  


while True:
    vals = getKeyboardInput()
    tello.send_rc_control(vals[0],vals[1],vals[2],vals[3])
    
    # print('Status | TOF=', tello.get_distance_tof())
    # print('Status | Height=', tello.get_height())

    # img = tello.get_frame_read().frame
    # img = cv2.resize(img, (360, 240))
    # cv2.imshow("Image", img)
    # cv2.waitKey(1)

    img = np.zeros((1000,1000, 3), np.uint8)
    if(points[-1][0]!=vals[4] or points[-1][1]!=vals[5]):
        points.append([vals[4],vals[5]])
    drawPoints(img, points)
    cv2.imshow("Output", img)
    cv2.waitKey(1)

    time.sleep(0.03)