import Tkinter as tk
import tkMessageBox as tkmb
import ttk
from functools import partial

import menus.mainmenu as mainmenu
import frames.logframe as logframe
import frames.fileframe as fileframe
import frames.cmdframe as cmdframe
import frames.outputframe as outputframe
import frames.exitframe as exitframe

from command import Command


class MainFrame(tk.Frame):

    def __init__(self, parent, *args, **kwargs):

        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        self.width = self.parent.winfo_screenwidth()
        self.height = self.parent.winfo_screenheight()
        self.parent.geometry('530x650+400+10')
        self.parent.title('VisualClient 0.7')
        self.parent.resizable(True, True)

        try:
            self.parent.iconbitmap('logo.ico')
        except:
            pass

        self.client = None

        self.main_menu = mainmenu.MainMenu(self)
        self.log_frame = logframe.LogFrame(self)
        self.file_frame = fileframe.FileTransferFrame(self)
        self.cmd_frame = cmdframe.CommandHandlerFrame(self)
        self.output_frame = outputframe.OutputFrame(self)
        self.exit_frame = exitframe.CloseExitFrame(self)

        self.parent.bind('<Return>', self._enter_pressed)

        self._button_config()
        self.parent.config(menu=self.main_menu)

        self.log_frame.pack()
        ttk.Separator(self, orient=tk.HORIZONTAL).pack(fill=tk.X)
        self.file_frame.pack()
        ttk.Separator(self, orient=tk.HORIZONTAL).pack(fill=tk.X)
        self.cmd_frame.pack()
        ttk.Separator(self, orient=tk.HORIZONTAL).pack(fill=tk.X)
        self.output_frame.pack()
        ttk.Separator(self, orient=tk.HORIZONTAL).pack(fill=tk.X)
        self.exit_frame.pack()

    def _enter_pressed(self, event):

        if self.focus_get() == self.file_frame.src_entry or self.focus_get() == self.file_frame.dst_entry:
            self.file_frame.ftf_button.focus_set()
            self.file_frame.ftf_button.invoke()

        elif self.focus_get() == self.cmd_frame.cmd_entry:
            self.cmd_frame.chf_button.focus_set()
            self.cmd_frame.chf_button.invoke()

        else:
            try:
                event.widget.invoke()
            except:
                pass

    def _button_config(self):
        """Configure buttons."""

        self.file_frame.ftf_button.config(command=self._ftf_command)
        self.cmd_frame.chf_button.config(command=self._chf_command)
        self.exit_frame.disconnect_button.config(command=partial(self._cef_command, '!EXIT'))
        self.exit_frame.close_button.config(command=partial(self._cef_command, '!CLOSE'))

    def _error_occurred(self):

        tkmb.showerror('Remote Server Error',
                       'Cannot communicate with server.\nServer might have closed.',
                       type=tkmb.OK)
        self.parent.destroy()

    def _ftf_command(self):

        mode, src, dst = self.file_frame.mode, self.file_frame.src_entry.get(), self.file_frame.dst_entry.get()

        if src is '' or dst is '':
            return None

        c = Command('!{} {} > {}'.format(mode, src, dst))
        try:
            if mode == 'SEND':
                update = self.client.send_cmd(c)
                self.log_frame.append_to_log('Send File:\n' + update)
            elif mode == 'GET':
                update = self.client.get_cmd(c)
                self.log_frame.append_to_log('Get File:\n' + update)
            else:
                pass
        except:
            self._error_occurred()

    def _chf_command(self):

        mode, cmd = self.cmd_frame.mode, self.cmd_frame.cmd_entry.get()

        if cmd is '':
            return None
        try:
            if mode == 'RAW':
                update = self.client.default_cmd(Command(cmd))
            elif mode == 'PRESET':
                update = ''
            else:
                update = ''
            self.output_frame.append_to_output(cmd, update)
        except:
            self._error_occurred()

    def _cef_command(self, command):

        try:
            self.client.exit_close_cmd(Command(command))
            self.parent.destroy()
        except:
            self._error_occurred()
