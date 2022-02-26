import socket
import tkinter
import threading
import time
import struct
from PIL import ImageGrab, Image, ImageTk
from zstd import decompress, Error


BUFFER_SIZE = 2**16

class Server:
    def __init__(self, ip, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((ip, port))

    def close(self):
        self.server_socket.close()

    def receive(self):
        data = b''
        while True:
            chunk, addr = self.server_socket.recvfrom(BUFFER_SIZE)
            if struct.unpack('B', chunk[:1])[0] > 1:
                data += chunk[1:]
            else:
                data += chunk[1:]
                break
        return data


class App:
    def __init__(self):
        # Initiate window
        self.tk = tkinter.Tk()
        self.tk.title("FPS: 0")
        self.tk.geometry("1768x992")
        self.tk.resizable(width = True, height = True)

        # Make a label on the screen for the image
        self.screen = tkinter.Label(self.tk)
        self.screen.pack()


    def start(self):
        ''' Start the app '''
        threading.Thread(target=self.screenshare, args=(), daemon=1).start() # Update the image on the screen with the latest image recieved
        self.tk.mainloop()


    def screenshare(self):
        ''' This fuction will recieve screenshot frame from the client and update it on the screen '''
        server = Server('localhost', 13370)
        counter = 0                # FPS COUNTER
        timeout = time.time() + 1  # FOR THE FPS COUNTER

        while True:
            try:
                frame = decompress(server.receive())
                counter = counter + 1 # FPS COUNTER

                w_width = self.tk.winfo_width()
                w_height = self.tk.winfo_height()

                image = Image.frombytes('RGB', (1920,1080), frame, 'raw', 'BGRX').resize((w_width, w_height))
                img = ImageTk.PhotoImage(image)
                self.screen.config(image=img)
                self.screen.image = img
            except Error as e:
                print(e)


            if time.time() > timeout: # AFTER A SECOND PASSES
                self.tk.title(f'FPS: {counter}')
                counter = 0
                timeout = time.time() + 1

            # When Over with the window self.tk.destroy()



def main():
    app = App()
    app.start()








if __name__ == '__main__':
    main()
