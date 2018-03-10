import tkinter
from queue import Empty
from View.scrollframe import ScrollableFrame


class MainWindow:
    """Main application window
    """
    def __init__(self, master, qin=None, qout=None):
        """Initialize MainWindow

        :param master: master widget
        :param qin: Queue for input queries
        :param qout: Queue for output queries
        """
        self.master = master
        self.qin = qin
        self.qout = qout
        self.active = True

        self.master.minsize(100, 100)
        self.master.protocol("WM_DELETE_WINDOW", self.iconify)
        self.output_frame = tkinter.Frame(master)
        self.sk_frame = ScrollableFrame(self.output_frame)
        self.field = tkinter.Entry(master, exportselection=0)
        self.field.bind("<Return>", lambda x: self.press())
        self.but = tkinter.Button(master, command=self.press, text='!', width=4)
        self.output_frame.grid(row=0, columnspan=2, sticky='NSWE')
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)
        self.but.grid(row=1, column=1)
        self.field.grid(row=1, column=0, sticky='WE')
        self.master.after(0, self.upd_output)

    def on_exit(self):
        """Action on exit
        """
        self.qin.put('exit')

    def press(self):
        """Action on button press
        """
        s = self.field.get()
        if len(s) > 0:
            self.sk_frame.present(s, my=True)
            self.qin.put(s)

    def iconify(self):
        """Iconify or deiconify window (hide it)
        """
        if self.active:
            self.master.withdraw()
            self.active = False
        else:
            self.master.deiconify()
            self.active = True

    def upd_output(self):
        """Check for signals, present messages
        """
        try:
            while True:
                s = self.qout.get(block=False)
                if s == "SIG_ICONIFY":
                    self.iconify()
                else:
                    self.present(s)
        except Empty:
            pass
        finally:
            self.master.after(10, self.upd_output)

    def present(self, arg):
        """Present object

        :param arg: Object to present
        """
        self.sk_frame.present(arg)
