import socket
import tkinter
import threading
import time
from PIL import ImageGrab, Image, ImageTk
from zlib import decompress

BUFFER_SIZE = 1024 * 8


class Server:
    def __init__(self, ip, port):
        self.server_socket = socket.socket()
        self.server_socket.bind((ip, port))
        self.server_socket.listen(1)
        print('Waiting for connections...')
        (self.client_socket, self.client_address) = self.server_socket.accept()
        print('Established connection...')

    def close(self):
        self.server_socket.close()

    def receive(self):
        chunk = self.client_socket.recv(BUFFER_SIZE)
        data = chunk
        while len(chunk) == BUFFER_SIZE:
            chunk = self.client_socket.recv(BUFFER_SIZE)
            data += chunk
        self.client_socket.sendall(b'\00')  # ack
        return data


class App:
    def __init__(self):
        # Initiate window
        self.tk = tkinter.Tk()
        self.tk.title("Remote Desktop")
        self.tk.geometry("1768x992")
        self.tk.resizable(width=True, height=True)

        # Make a label on the screen for the image
        self.label = tkinter.Label(self.tk)
        self.label.pack()

    def start(self):
        ''' Start the app '''
        threading.Thread(target=self.screenshare, args=(), daemon=1).start()  # Update the image on the screen with the latest image recieved
        self.tk.mainloop()

    def screenshare(self):
        ''' This fuction will recieve screenshot frame from the client and update it on the screen '''
        server = Server('localhost', 13370)
        counter = 0  # FPS COUNTER
        timeout = time.time() + 1  # FOR THE FPS COUNTER
        while True:
            frame = decompress(server.receive())
            counter = counter + 1  # FPS COUNTER
            f_width = int(server.receive().decode())
            f_height = int(server.receive().decode())

            w_width = self.tk.winfo_width()
            w_height = self.tk.winfo_height()

            image = Image.frombytes('RGB', (f_width, 1080), frame).resize((w_width, w_height))
            img = ImageTk.PhotoImage(image)
            self.label.config(image=img)
            self.label.image = img

            if time.time() > timeout: # AFTER A SECOND PASSES
                self.tk.title(f'FPS: {counter}')
                counter = 0
                timeout = time.time() + 1

def main():
    app = App()
    app.start()


if __name__ == '__main__':
    main()
