import socket
import struct
import sys
sys.path.append("../python-ev3-master/")
from ev3.rawdevice.lms2012 import TYPE_TACHO, TYPE_NONE
from ev3.rawdevice import motordevice


UDP_IP = "10.0.1.1"
UDP_PORT = 6543

MAX_SPEED = 80
MIN_SPEED = 5
LEFT_FRONT_PORT = (0x01)  # A
RIGHT_FRONT_PORT = (0x02) # B
LEFT_BACK_PORT = (0x04) # C
RIGHT_BACK_PORT = (0x08) # D
PORTS = (0x0F)


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

motordevice.open_device()
motordevice.set_types([TYPE_NONE, TYPE_TACHO,TYPE_TACHO ,TYPE_NONE ])
motordevice.reset(PORTS)

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    data_len = len(data)
    # data structure: lX, lY, lZ, lRx, lRy, lRz, rglSlider0, rglSlider1, rgdwPOV0, rgdwPOV1, rgdwPOV2, rgdwPOV3, button numbers...
    # First 8 values are long, following 4 values are unsigned long, following are byte array of pressed button
    # I know hard-coded value are ugly, let's fix it later. This is an hackson, ok?
    rv = struct.unpack('llllllllLLLL'+'B'*(data_len - 12*4), data)
    direction = rv[4] # -1000 full speed forward, +1000 full speed backward
    turn = rv[0] # -1000 full speed left turn, +1000 full speed right turn
   
    if turn >= 0:
        left_speed = ((float)(MAX_SPEED)/1000) * (-direction)
        right_speed = ((float)(-2)/1000) * left_speed * turn + left_speed
    else:
        right_speed = ((float)(MAX_SPEED)/1000) * (-direction)
        left_speed = ((float)(2)/1000) * right_speed * turn + right_speed
    print "dir:", direction, "turn:", turn
    left_front_speed = int(-left_speed)
    left_front_speed = 0 if abs(left_front_speed) < MIN_SPEED else left_front_speed
    left_front_speed = left_front_speed + 0xFF if left_front_speed < 0 else left_front_speed
    right_front_speed = int(-right_speed)
    right_front_speed = 0 if abs(right_front_speed) < MIN_SPEED else right_front_speed
    right_front_speed = right_front_speed + 0xFF if right_front_speed < 0 else right_front_speed
    left_back_speed = int(left_speed)
    left_back_speed = 0 if abs(left_back_speed) < MIN_SPEED else left_back_speed
    left_back_speed = left_back_speed + 0xFF if left_back_speed < 0 else left_back_speed
    right_back_speed = int(right_speed)
    right_back_speed = 0 if abs(right_back_speed) < MIN_SPEED else right_back_speed
    right_back_speed = right_back_speed + 0xFF if right_back_speed < 0 else right_back_speed
    motordevice.speed(LEFT_FRONT_PORT, left_front_speed)
    motordevice.speed(RIGHT_FRONT_PORT, right_front_speed)
    motordevice.speed(LEFT_BACK_PORT, left_back_speed)
    motordevice.speed(RIGHT_BACK_PORT, right_back_speed)
