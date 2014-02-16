import socket

FROM_IP = "192.168.235.1"
FROM_PORT = 6543
TO_IP = "10.0.1.1"
TO_PORT = 6543

BUFFER_SIZE = 1024

from_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
from_sock.bind((FROM_IP, FROM_PORT))
to_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
to_sock.connect((TO_IP, TO_PORT))

while True:
    try:
        data, addr = from_sock.recvfrom(BUFFER_SIZE) # buffer size is 1024 bytes
        to_sock.send(data)
        print "Relayed:", data
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        print "Some exception happens! Who cares."

from_sock.close()
