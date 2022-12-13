# PID (Proportional Integral Derivative) to reduce overshooting
import cv2, time
import numpy as np
from djitellopy import Tello


tello = Tello()
tello.connect()
print('Status | Battery=', tello.get_battery())

tello.takeoff()
tello.send_rc_control(0, 0, 0, 0)
time.sleep(2.5)


w, h = 360, 240
fbRange = [5900, 6500]
pid = [0.4, 0.4, 0]
pError = 0

def findFace(img):
    faceCascade = cv2.CascadeClassifier('C:\\Users\\kevingao\\workspace\\H\\Enactive\\TelloPet\\projects\\resources\\haarcascade_frontalface_default.xml')
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # img_path = os.path.join('C:\\Users\\kevingao\\workspace\\H\\Enactive\\TelloPet\\projects', img)
    # img_array = cv2.imread(img_path)
    faces = faceCascade.detectMultiScale(imgGray,1.1,6)

    myFaceListC = []
    myFaceListArea = []
 
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        cx = x + w//2
        cy = y + h//2
        area = w*h
        myFaceListArea.append(area)
        myFaceListC.append([cx,cy])
 
    if len(myFaceListArea) !=0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i],myFaceListArea[i]]
    else:
        return img,[[0,0],0]


def trackFace(tello, info,w,pid,pError):
    fb = 0
    x,y = info[0]
    area = info[1]
    ## PID
    error = x - w//2
    speed = pid[0]*error + pid[1]*(error-pError)
    speed = int(np.clip(speed,-100,100))

    if area > fbRange[0] and area < fbRange[1]:
        fb = 0
    elif area > fbRange[1]:
        fb = -20
    elif area < fbRange[0] and area!= 0:
        fb = 20
    if x == 0:
        speed = 0
        error = 0

    print('error', error, 'fb', fb)
    tello.send_rc_control(0, fb, 0, speed)

    return error


tello.streamon() # EDU no support when connected to wifi

# cap = cv2.VideoCapture(1) # From pc camera
while True:
    # _, img = cap.read()
    img = tello.get_frame_read().frame # From drone
    img = cv2.resize(img, (w, h))
    img, info = findFace(img)
    print("center", info[0], "area", info[1])
    pError = trackFace(tello, info,w,pid,pError)
    cv2.imshow("output", img) 
    cv2.waitKey(1)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        tello.land()
        break



 