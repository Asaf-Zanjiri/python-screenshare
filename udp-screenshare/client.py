import socket
import mss
import math
import struct
from zstd import compress

BUFFER_SIZE = (2**16)-64

class Client:
    def __init__(self, addr, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.addr = addr
        self.port = port

    def close(self):
        self.client_socket.close()

    def send(self, image):
        size = len(image)
        num_of_chunks = math.ceil(size/(BUFFER_SIZE))
        array_pos_start = 0

        while num_of_chunks:
            array_pos_end = min(size, array_pos_start + BUFFER_SIZE)
            self.client_socket.sendto(struct.pack('B', num_of_chunks) + image[array_pos_start:array_pos_end], (self.addr, self.port))
            array_pos_start = array_pos_end
            num_of_chunks = num_of_chunks-1

def grab_screenshot(sct, monitor=1):
    ''' The function will take a screenshot of the monitor and return sct,resolution '''
    img = sct.grab(sct.monitors[monitor])
    return img.bgra



def main():
    client = Client('127.0.0.1', 13370)
    sct = mss.mss()

    while True:
        frame = grab_screenshot(sct)
        client.send(compress(frame, 9))



if __name__ == '__main__':
    main()