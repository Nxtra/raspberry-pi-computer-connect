import pickle
import struct
import socket


def send(s, data):
    data = pickle.dumps(data)
    s.sendall(struct.pack('>i', len(data)))
    s.sendall(data)


def recv(s):
    data = s.recv(4, socket.MSG_WAITALL)
    data_len = struct.unpack('>i', data)[0]
    print("Data len is {}".format(data_len))
    data = s.recv(data_len, socket.MSG_WAITALL)
    return pickle.loads(data)


def ask_input():
    return input('Type message you want to send: ')


if __name__ == "__main__":
    # Create server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', 9395))
    s.listen(10)
    # Accept a client
    conn, addr = s.accept()
    print('connected to client')
    # conn is now a "socket", if you write to it, the client receives that data.
    # If you read from it, you get what the client sent you

    while True:
        incoming_data = recv(conn)
        print("New message received: \n{}".format(incoming_data))
        reply = ask_input()
        send(conn, reply)
