import Tkinter as tk


class HelpMenu(tk.Menu):

    def __init__(self, parent, *args, **kwargs):

        tk.Menu.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        self.add_command(label='Manual', command=lambda: True)
        self.add_command(label='About', command=lambda: True)
