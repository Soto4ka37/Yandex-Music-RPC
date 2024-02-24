from wx import App

from gui.main_window import MainWindow
from gui.controller import gui

from modules.data import data
from modules.single_instance import single_instance, cleanup

app = App()
single_instance()

gui.main = MainWindow(None)
app.MainLoop()

# После закрытия основного окна

data.save()

cleanup()