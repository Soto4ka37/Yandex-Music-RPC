import wx

from os import O_CREAT, O_EXCL, O_RDWR, getpid, write, close, unlink, remove, open as os_open
from sys import exit

from modules.data import LOCK_FILE, LOGO

class InfoDialog(wx.Dialog):
    def __init__(self, parent, title, message):
        super(InfoDialog, self).__init__(parent, title=title)

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetIcon(wx.Icon(LOGO))

        message_label = wx.StaticText(panel, label=message)
        vbox.Add(message_label, 0, wx.ALL | wx.EXPAND, 20)

        btn_continue = wx.Button(panel, label='Продолжить')
        btn_continue.Bind(wx.EVT_BUTTON, self.on_continue)
        btn_exit = wx.Button(panel, label='Выход')
        btn_exit.Bind(wx.EVT_BUTTON, self.on_exit)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(btn_continue, 0, wx.ALL, 10)
        hbox.Add(btn_exit, 0, wx.ALL, 10)

        vbox.Add(hbox, 0, wx.ALIGN_CENTER)
        panel.SetSizer(vbox)

        self.SetSize((400, 150))
        self.Centre()

    def on_continue(self, event):
        self.EndModal(wx.ID_OK)

    def on_exit(self, event):
        self.EndModal(wx.ID_CANCEL)


def single_instance():
    try:
        lock_fd = os_open(LOCK_FILE, O_CREAT | O_EXCL | O_RDWR)
    except FileExistsError:
        dialog = InfoDialog(None, 'Приложение уже открыто', message='Приложение уже открыто или было завершено неккоректно!')
        result = dialog.ShowModal()
        dialog.Destroy()
        if result == wx.ID_CANCEL:
            exit()
    else:
        write(lock_fd, str(getpid()).encode())
        close(lock_fd)

def cleanup():
    try: unlink(LOCK_FILE); remove(LOCK_FILE)
    except: pass