import os
#import keyboard
import winsound
import importlib.util
import types
import socket


def run_method(filename, method_name):
    """Run method :method_name: from :filename:

    Run method without arguments and yield output

    :param filename: File, where to look for method
    :param method_name: Name of method to run
    :return: Generator with first 'started' mark and then outputs
    """
    # yield 'run_method started'
    try:
        spec = importlib.util.spec_from_file_location(method_name, filename)
        module = importlib.util.module_from_spec(spec)
        # yield 'module defined'
        spec.loader.exec_module(module)
        # yield 'exec_module ended'

        yield str(method_name) + ' started'
        ans = getattr(module, method_name)()
    except Exception as e:
        ans = ['Exception:', e]
    if isinstance(ans, types.GeneratorType):
        for a in ans:
            yield a
    else:
        yield ans
#run method get_command_list from Lib/core_functions.py


def get_command_list():
    """Get command to show example of possible tasks

    :return: tuple[2]
    """
    return 'exec', 'self.q_out.put([t.example for t in self.possible_tasks])'


def get_active_processes():
    """Get command to show names of active processes

    :return: tuple[2]
    """
    return 'exec', 'self.q_out.put(["Active processes:"] + [pr.name for pr in active_children()])'


# DEPRECATED
'''def bind_gui():
    """Wait for pressing Ctrl+Shift+a to send signal to iconify window

    :return: Generator with 'SIG_ICONIFY'
    """
    while True:
        keyboard.wait('ctrl+shift+a')
        winsound.PlaySound('Notify.wav', winsound.SND_FILENAME)
        yield 'SIG_ICONIFY'
'''


def socket_activation():
    """Wait `b'show'` to socket localhost:8887 then send `'SIG_DEICONIFY'`

    :return: Generator with 'SIG_DEICONIFY'
    """
    a = socket.socket()
    a.bind(('localhost', 8887))
    a.listen(5)
    while True:
        ns, adrr = a.accept()
        # print(adrr, ns, sep='\n')
        # print('Connection opened')
        ns.settimeout(5)
        data = ns.recv(256)
        while len(data) > 0:
            # data = str(data)
            commands = data.split(b'\n')
            for c in commands:
                if len(c) > 0:
                    # print('Received command:', c)
                    if c == b'show':
                        winsound.PlaySound('Notify.wav', winsound.SND_FILENAME)
                        yield 'SIG_DEICONIFY'
            data = ns.recv(256)
        # print('Connection closed')


def terminate_process_by_name(name):
    """Get command to terminate process

    Terminate all processes with same name

    :param name: name of process (same as command cause it)
    :return: tuple[2]
    """
    return 'exec', '''
for p in active_children():
    if p.name == '{0}':
        self.q_out.put('Terminate ' + p.name)
        p.terminate()
'''.format(name)


def restart():
    """Get command to restart app

    Start new instance of application and self-terminates

    :return: tuple[2]
    """
    os.startfile('Win.bat')
    return close_app()

def close_app():
    """Get command to close application

    :return: tuple[2]
    """
    return 'exec', '''
self.terminate()'''


if __name__ == '__main__':
    # print(terminate_process_by_name('Pr'))
    for i in run_method('net.py', 'parse_wiki'):
        print(i)
