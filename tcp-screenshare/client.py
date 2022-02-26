import socket
import mss
from PIL import Image
from zlib import compress

BUFFER_SIZE = 1024 * 8

class Client:
    def __init__(self, ip, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((ip, port))
        print('Connected successfully to the server')

    def close(self):
        self.client_socket.close()

    def send(self, message):
        self.client_socket.sendall(message)
        ack = self.client_socket.recv(1)

def grab_screenshot(monitor=1):
    ''' The function will take a screenshot of the monitor and return sct,resolution '''
    sct = mss.mss()
    img = sct.grab(sct.monitors[monitor]) # Grab a screenshot of the 1st monitor
    return Image.frombytes('RGB', img.size, img.bgra, 'raw', 'BGRX').tobytes(), (img.size.width, img.size.height)

def main():
    client = Client('127.0.0.1', 13370)
    while True:
        frame, resolution = grab_screenshot()
        client.send(compress(frame, 9))             # Send compressed screenshot
        client.send(str(resolution[0]).encode())    # Send width
        client.send(str(resolution[1]).encode())    # Send height
    




if __name__ == '__main__':
    main()