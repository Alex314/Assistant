from multiprocessing import Process, Queue, active_children
from main_window import MainWindow
import tkinter
from queue import Empty
import importlib.util


def process_query(query, out_queue):
    if query in ['exit', 'close', 'выход', 'выйти', 'закрыть']:
        print('exit')
        children = active_children()
        print(children)
        for ch in children:
            ch.terminate()
            print(ch)
        return 0
    elif query.isnumeric():
        Process(target=run_function, args=(
                out_queue, r'factorial.py',
                'factorial', *(int(query), ))).start()
    return 1


def run_function(out_queue, path, function_name, *args):
    spec = importlib.util.spec_from_file_location(function_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    ans = getattr(module, function_name)(*args)
    out_queue.put(ans)


def window_input(qin, qout):
    root = tkinter.Tk()
    MainWindow(root, qin, qout)
    root.mainloop()


def main_loop(comp, inp, outp):
    while True:
        try:
            while True:
                s = comp.get(block=False)
                outp.put(s)
        except Empty:
            pass
        try:
            while True:
                s = inp.get(block=False)
                if not process_query(s, comp):
                    return 0
        except Empty:
            pass


if __name__ == '__main__':
    comp = Queue()
    comp.cancel_join_thread()
    inp = Queue()
    outp = Queue()
    input_proc = Process(target=window_input, args=(inp, outp), name='GUI')
    input_proc.start()
    main_loop(comp, inp, outp)
