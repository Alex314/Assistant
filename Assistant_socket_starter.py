import socket
from core import run


def connect():
    """Open socket and connect to `localhost:8887`

    may rise ConnectionRefusedError if not responsive
    :return: socket
    """
    a = socket.socket()
    a.connect(('localhost', 8887))
    return a


def start():
    """Try to send `b'show'` to `localhost:8887` else start new Assistant instance
    """
    try:
        a = connect()
        a.send(b'show\n')
    except ConnectionRefusedError:
        run()


if __name__ == '__main__':
    start()
