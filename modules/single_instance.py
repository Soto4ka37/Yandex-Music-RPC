import os

from wx import Dialog, Panel, BoxSizer, StaticText, Button, VERTICAL, ALL, EXPAND, EVT_BUTTON, HORIZONTAL, ALIGN_CENTER, ID_OK, ID_CANCEL, Icon
from modules.data import LOCK_FILE, LOGO
from sys import exit

class InfoDialog(Dialog):
    def __init__(self, parent, title, message):
        super(InfoDialog, self).__init__(parent, title=title)

        panel = Panel(self)
        vbox = BoxSizer(VERTICAL)
        self.SetIcon(Icon(LOGO))

        message_label = StaticText(panel, label=message)
        vbox.Add(message_label, 0, ALL | EXPAND, 20)

        btn_continue = Button(panel, label='Продолжить')
        btn_continue.Bind(EVT_BUTTON, self.on_continue)
        btn_exit = Button(panel, label='Выход')
        btn_exit.Bind(EVT_BUTTON, self.on_exit)
        hbox = BoxSizer(HORIZONTAL)
        hbox.Add(btn_continue, 0, ALL, 10)
        hbox.Add(btn_exit, 0, ALL, 10)

        vbox.Add(hbox, 0, ALIGN_CENTER)
        panel.SetSizer(vbox)

        self.SetSize((400, 150))
        self.Centre()

    def on_continue(self, event):
        self.EndModal(ID_OK)

    def on_exit(self, event):
        self.EndModal(ID_CANCEL)


def single_instance():
    try:
        lock_fd = os.open(LOCK_FILE, os.O_CREAT | os.O_EXCL | os.O_RDWR)
    except FileExistsError:
        dialog = InfoDialog(None, 'Приложение уже открыто', message='Приложение уже открыто или было завершено неккоректно!')
        result = dialog.ShowModal()
        dialog.Destroy()
        if result == ID_CANCEL:
            exit()
    else:
        os.write(lock_fd, str(os.getpid()).encode())
        os.close(lock_fd)

def cleanup():
    try: os.unlink(LOCK_FILE); os.remove(LOCK_FILE)
    except: pass