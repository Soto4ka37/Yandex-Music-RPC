from wx import App
app = App()

from modules.update import check_updates

check_updates()

from gui.main_window import MainWindow
from gui.controller import gui

from modules.data import data
from modules.single_instance import single_instance, cleanup

single_instance()

gui.main = MainWindow(None)
app.MainLoop()

# После закрытия основного окна

data.save()

cleanup()