import socket
import pickle
import struct

# SenseHat
from sense_hat import SenseHat

sense = SenseHat()


def send(s, data):
    data = pickle.dumps(data)
    s.sendall(struct.pack('>i', len(data)))
    s.sendall(data)


def recv(s):
    data = s.recv(4, socket.MSG_WAITALL)
    data_len = struct.unpack('>i', data)[0]
    data = s.recv(data_len, socket.MSG_WAITALL)
    return pickle.loads(data)


def read_sensehat():
    acceleration = sense.get_accelerometer_raw()
    ax = acceleration['x']
    ay = acceleration['y']
    az = acceleration['z']

    orientation_rad = sense.get_orientation_radians()
    pitch = orientation_rad.get('pitch')
    roll = orientation_rad.get('roll')
    yaw = orientation_rad.get('yaw')

    list_of_sensehat_readings = [ax, ay, az, pitch, roll, yaw]
    list_of_sensehat_readings_strings = [str(round(i, 5)) for i in list_of_sensehat_readings]
    readings = ','.join(list_of_sensehat_readings_strings)
    return readings


class Pixel:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def drawPixel(self):
        sense.clear()
        sense.set_pixel(self.x, self.y, (255, 0, 0))

    def setPixel(self, x, y):
        self.x = x
        self.y = y


if __name__ == "__main__":
    # Create server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', 9395))
    s.listen(10)

    redDot = Pixel(1, 1)
    # Accept a client
    conn, addr = s.accept()
    print('Got connection from', addr)

    while True:
        msg = recv(conn)
        print('Pixel placed at', msg.x, ',', msg.y)
        redDot.setPixel(msg.x, msg.y)
        redDot.drawPixel()
        readings = read_sensehat()
        print(f"This are my readings: {readings}")
        print("Sending readings to client")
        send(conn, readings)