from djitellopy import Tello
import time, cv2

tello = Tello()

tello.connect()

print('Status | Battery=', tello.get_battery())

tello.streamon()

while True:
    img = tello.get_frame_read().frame
    img = cv2.resize(img, (1024, 1024))
    cv2.imshow("Image", img)
    cv2.waitKey(1)



