import tkinter
from queue import Empty


class MainWindow:
    def __init__(self, master, qin=None, qout=None):
        self.master = master
        self.qin = qin
        self.qout = qout

        master.minsize(100, 100)
        master.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.text = tkinter.Text(master)
        self.field = tkinter.Entry(master)
        self.field.bind("<Return>", lambda x: self.press())
        self.but = tkinter.Button(master, command=self.press, text='!', width=4)
        self.text.grid(row=0, columnspan=2, sticky='NSWE')
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)
        self.but.grid(row=1, column=1)
        self.field.grid(row=1, column=0, sticky='WE')
        self.master.after(0, self.upd_output)

    def on_exit(self):
        self.qin.put('exit')

    def press(self):
        s = self.field.get()
        if len(s) > 0:
            self.text.insert(tkinter.END, s + '\n')
            self.text.see(tkinter.END)
            self.qin.put(s)
            if s == 'exit':
                exit(0)

    def upd_output(self):
        try:
            while True:
                s = self.qout.get(block=False)
                self.present(s)
                self.text.see(tkinter.END)
        except Empty:
            pass
        finally:
            self.master.after(10, self.upd_output)

    def present(self, arg):
        if type(arg) is type(list()):
            for i in arg:
                self.present(i)
            self.present('')
        else:
            self.text.insert(tkinter.END, arg.__str__() + '\n')

