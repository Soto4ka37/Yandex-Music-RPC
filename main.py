from gui.main_window import MainWindow
from gui.controller import gui
from wx import App

from modules.data import data
from modules.single_instance import single_instance, cleanup
app = App()

single_instance() # Проверяем запущено ли приложение

gui.main = MainWindow(None)
app.MainLoop() # Запускаем основное окно

# По закрытии основного окна сохраняем данные

data.save()

cleanup()