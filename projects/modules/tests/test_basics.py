from djitellopy import Tello
import time

tello = Tello()

tello.connect()
tello.takeoff()

time.sleep(2)

# tello.move_forward(20)
# tello.move_back(20)


tello.rotate_clockwise(360)
# tello.rotate_counter_clockwise(90)
tello.rotate_counter_clockwise(90)

tello.move_forward(50)

# tello.send_rc_control(0,30,0,0)

# time.sleep(2)

# tello.send_rc_control(0,-30,0,0)

# time.sleep(2)

# tello.send_rc_control(-30,0,0,0)

# time.sleep(2)

# tello.send_rc_control(30,0,0,0)

# time.sleep(2)

# tello.send_rc_control(0,0,0,0) # stop completely

time.sleep(2)

print(tello.get_distance_tof())

tello.land()