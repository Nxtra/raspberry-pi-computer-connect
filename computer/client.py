import pickle
import struct

import socket

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


def ask_input():
    return input('Type message you want to send: ')


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    s.connect((RASPBERRY_PI_IP, 9395))

    # s is  now a "socket"
    while True:
        data = ask_input()
        send(s, data)
        incoming_message = recv(s)
        print(incoming_message)
