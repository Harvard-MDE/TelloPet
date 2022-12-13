from djitellopy import Tello
import time

tello = Tello()

tello.connect()

print('Status | Battery<=', tello.get_battery())

print('Status | Temperature<=', tello.get_highest_temperature())

print('Status | TOF=', tello.get_distance_tof())

print('Status | Height=', tello.get_height())

print('Info | Video address =', tello.get_udp_video_address())

