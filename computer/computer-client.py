import socket
import pickle
import struct
import time

RASPBERRY_PI_IP = '192.168.1.22'


def send(s, data):
    data = pickle.dumps(data)
    s.sendall(struct.pack('>i', len(data)))
    s.sendall(data)


def recv(s):
    data = s.recv(4, socket.MSG_WAITALL)
    data_len = struct.unpack('>i', data)[0]
    data = s.recv(data_len, socket.MSG_WAITALL)
    return pickle.loads(data)


def get_webcam_data():
    None


class Pixel:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    s.connect((RASPBERRY_PI_IP, 9395))

    while True:
        # At the moment you, as a person, are giving the action here
        x_val = input("X: ")
        y_val = input("Y: ")
        msg = Pixel(x_val, y_val)
        send(s, msg)
        print('Pixel placed at', msg.x, ',', msg.y)
        incoming_state_data_accelero_and_gyro = recv(s)
        print(f'Incoming data: {incoming_state_data_accelero_and_gyro}')
