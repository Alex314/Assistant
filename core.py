from multiprocessing import Process, Queue
from main_window import MainWindow
import tkinter
from task_processor import TaskProcessor


def window_input(q_in, q_out):
    root = tkinter.Tk()
    MainWindow(root, q_in, q_out)
    root.mainloop()


if __name__ == '__main__':
    comp = Queue()
    comp.cancel_join_thread()
    inp = Queue()
    outp = Queue()
    input_proc = Process(target=window_input, args=(inp, outp), name='GUI')
    input_proc.start()
    TaskProcessor(inp, outp).run()
