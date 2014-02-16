import socket
import struct

UDP_IP = "127.0.0.1"
UDP_PORT = 6543

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    data_len = len(data)
    # data structure: lX, lY, lZ, lRx, lRy, lRz, rglSlider0, rglSlider1, rgdwPOV0, rgdwPOV1, rgdwPOV2, rgdwPOV3, button numbers...
    # First 8 values are long, following 4 values are unsigned long, following are byte array of pressed button
    # I know hard-coded value are ugly, let's fix it later. This is an hackson, ok?
	rv = struct.unpack('llllllllLLLL'+'B'*(data_len - 12*4), data)
    print rv
