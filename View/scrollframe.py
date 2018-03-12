import tkinter as tk
from time import strftime, localtime


class ScrollableFrame:
    """Canvas with frame and scrollbar
    """
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, bg='gray')
        self.frame = tk.Frame(self.canvas, bg='gray')
        self.frame.grid_columnconfigure(0, weight=1)
        self.myscrollbar = tk.Scrollbar(master, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.myscrollbar.set)
        self.myscrollbar.pack(side="right", fill="y")
        self.canvas.pack(expand=True, fill="both")
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.frame)
        self.canvas.bind("<Configure>", self.canvas_configure)
        self.frame.bind("<Configure>", self.frame_configure)

    def canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

    def frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def present(self, obj, my=False):
        """Show object at frame

        :param obj: Object to show
        :param my -> bool: Is it my message (shows left)
        """
        mes = Message(self.frame, right=my)
        mes.present(obj)
        self.master.after(100, lambda: self.canvas.yview_moveto(1))


class Message:
    """Widget to represent messages
    """
    def __init__(self, master, right=True):
        """Initialize Message

        :param master: master widget
        :param right -> bool: Show at right or left side
        """
        self.master = master
        self.frame = tk.Frame(self.master, borderwidth=2)
        self.frame.grid(sticky='NW' if right else 'NE', pady=1)

    def add_text(self, text):
        """Add text to message

        :param text: text to add
        """
        tk.Label(self.frame, text=text).grid(sticky='NW')
        '''txt = tk.Text(self.frame, width=len(text), height=1)
        txt.insert(tk.END, text)
        txt.grid(sticky='NW')'''

    def add_obj(self, obj):
        """Add object or list to Message frame

        Tuple or list adds element-wise
        :param obj: object to show in Message
        """
        if isinstance(obj, (tuple, list)):
            for o in obj:
                self.add_obj(o)
        else:
            self.add_text(str(obj))

    def present(self, obj):
        """Add object to Message

        Tuple or list adds element-wise
        :param obj: object (list, tuple) to show
        """
        self.add_obj(obj)
        tk.Label(self.frame, font='Arial 7',
                 text=strftime("%H:%M:%S", localtime())).grid(column=1, row=self.frame.grid_size()[1] - 1, sticky='SE')
