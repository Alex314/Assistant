import os


def get_command_list():
    return 'exec', 'self.q_out.put([t.example for t in self.possible_tasks])'


def get_active_processes():
    return 'exec', 'self.q_out.put(["Active processes:"] + [pr.name for pr in active_children()])'


def terminate_process_by_name(name):
    return 'exec', '''
for p in active_children():
    if p.name == '{0}':
        self.q_out.put('Terminate ' + p.name)
        p.terminate()
'''.format(name)


def restart():
    os.startfile('Win.bat')
    return 'exec', '''
self.terminate()'''

def close_app():
    return 'exec', '''
self.terminate()'''


if __name__ == '__main__':
    print(terminate_process_by_name('Pr'))
