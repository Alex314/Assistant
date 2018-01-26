from multiprocessing import Process, Queue, active_children
from main_window import MainWindow
import tkinter
from queue import Empty
import subprocess


def f(i, qu):
    try:
        result = subprocess.run(
            ['python', 'factorial.py', str(i)],
            stdout=subprocess.PIPE)
        ans = [i, result.stdout.decode('utf-8').rstrip()]
        qu.put(ans)
    except Exception as e:
        pass
        #print('Ouch, Exception:')
        #print(e.args)


def window_input(qin, qout):
    root = tkinter.Tk()
    MainWindow(root, qin, qout)
    root.mainloop()


def main_loop(comp, inp, outp, pp):
    while True:
        try:
            while True:
                s = comp.get(block=False)
                outp.put(s[1])
        except Empty:
            pass
        try:
            while True:
                s = inp.get(block=False)
                if s in ['exit', 'close', 'выход', 'выйти', 'закрыть']:
                    print('exit')
                    children = active_children()
                    print(children)
                    for ch in children:
                        ch.terminate()
                        print(ch)
                    return 0
                elif s.isnumeric():
                    pp += [(Process(target=f, args=(int(s), comp)), int(s))]
                    pp[-1][0].start()
        except Empty:
            pass


if __name__ == '__main__':
    comp = Queue()
    comp.cancel_join_thread()
    inp = Queue()
    outp = Queue()
    input_proc = Process(target=window_input, args=(inp, outp), name='GUI')
    input_proc.start()
    pp = []
    main_loop(comp, inp, outp, pp)
