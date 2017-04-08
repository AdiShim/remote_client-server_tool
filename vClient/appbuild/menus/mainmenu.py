import Tkinter as tk

import helpmenu


class MainMenu(tk.Menu):

    def __init__(self, parent, *args, **kwargs):

        tk.Menu.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        self.help_menu = helpmenu.HelpMenu(self)

        self.add_cascade(label='Help', menu=self.help_menu)
