import Tkinter as tk
from functools import partial


class CommandHandlerFrame(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        """Class constructor."""

        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.mode = 'RAW'

        tk.Radiobutton(self, text='Command', value=1, variable='chf',
                       command=partial(self._change_mode, 'RAW')).grid(row=0, column=0, sticky=tk.W, pady=(5, 0))
        tk.Radiobutton(self, text='Preset ID', value=2, variable='chf',
                       command=partial(self._change_mode, 'PRESET')).grid(row=1, column=0, sticky=tk.W)

        self.cmd_entry = tk.Entry(self)
        self.cmd_entry.grid(row=0, column=2, sticky=tk.E, padx=(0, 5), pady=(5, 0))

        # self.chf_button command is configured in mainframe.py
        self.chf_button = tk.Button(self, text='SEND')
        self.chf_button.grid(columnspan=3, row=2, column=0, pady=(0, 5))

    def _change_mode(self, change_to):
        """Change self.mode from RAW to PRESET or vice versa."""

        self.mode = change_to


def main():
    root = tk.Tk()
    CommandHandlerFrame(root).pack()
    root.mainloop()

if __name__ == '__main__':
    main()
