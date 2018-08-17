import socket
from core import run


def connect():
    a = socket.socket()
    a.connect(('localhost', 8887))
    return a


def start():
    try:
        a = connect()
        a.send(b'show\n')
    except ConnectionRefusedError:
        run()


if __name__ == '__main__':
    start()
