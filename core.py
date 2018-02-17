"""Main module of the Assistant"""

import tkinter
from multiprocessing import Process, Queue

from main_window import MainWindow
from task_processor import TaskProcessor


def window_input(q_in: Queue, q_out: Queue):
    """Open main window

    :param q_in: Queue for input messages
    :param q_out: Queue for output messages
    """
    root = tkinter.Tk()
    MainWindow(root, q_in, q_out)
    root.mainloop()


def run():
    """Run main loop of assistant"""
    comp = Queue()
    comp.cancel_join_thread()
    inp = Queue()
    outp = Queue()
    input_proc = Process(target=window_input, args=(inp, outp), name='GUI')
    input_proc.start()
    TaskProcessor(inp, outp).run()


if __name__ == '__main__':
    run()
