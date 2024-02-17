from wx import Frame, Panel, CheckBox,  StaticBitmap, StaticText, StaticLine, Event, Button, Icon, Menu, Image as WxImage, CallAfter
from wx import EVT_CLOSE, ID_ANY, WHITE, EVT_CHECKBOX, EVT_BUTTON, LI_HORIZONTAL, NullBitmap, CallAfter, EVT_MENU
from wx.adv import TaskBarIcon, EVT_TASKBAR_LEFT_DOWN, EVT_TASKBAR_RIGHT_DOWN
from modules.data import VERSION, LOGO
from requests import get
from io import BytesIO
from PIL import Image

from threading import Thread
from traceback import format_exc

from gui.settings import Settings
from gui.controller import gui
from modules.formate import formate_string
from modules.debugger import debugger
from modules.data import data
from modules.yandex import api
from modules.discord import rpc

class MainWindow(Frame):
    def __init__(self, parent = None):
        Frame.__init__(self, parent, title=f"RPC {VERSION}", size=(350, 130))
        self.panel = Panel(self)
        self.panel.SetBackgroundColour(WHITE)
        self.Bind(EVT_CLOSE, self.close)
        self.tray_icon = TrayIcon(self)
        self.SetIcon(Icon(LOGO))
        self.checkbox = CheckBox(self.panel, label='Подключиться', pos=(90, 10))
        self.checkbox.Bind(EVT_CHECKBOX, self.connect)

        button = Button(self.panel, label="Параметры", pos=(200, 8), size=(130, 20))
        button.Bind(EVT_BUTTON, self.open_settings)

        self.line = StaticLine(self.panel, ID_ANY, pos=(90, 35), size=(240, 1), style=LI_HORIZONTAL)

        self.title = StaticText(self.panel, label='Отлючено', pos=(95, 43))
        self.author = StaticText(self.panel, label='', pos=(95, 60))
        
        self.icon = StaticBitmap(self.panel, bitmap=NullBitmap, pos=(5, 5))
        
        self.Show(True)
        self.checkbox.SetValue(data.auto_connect)
        if self.checkbox.GetValue():
            self.connect(event=None)
        self.update_icon('https://cdn.discordapp.com/attachments/1117022431748554782/1117022461045772379/logo.png')
        
    def force_disconnect(self, reason: str):
        self.checkbox.SetValue(False)
        rpc.stop_autoupdate()
        api.stop_autoupdate()
        self.title.SetLabelText('Произошла ошибка, подробнее в меню отладки')
        self.author.SetLabelText(reason)
        self.update_icon('https://cdn.discordapp.com/attachments/1117022431748554782/1117022461045772379/logo.png')

    def connect(self, event: Event):
        checkbox = self.checkbox
        if checkbox.GetValue():
            debugger.addInfo('Пользователь активировал программу')
            self.title.SetLabelText('Загрузка...')
            self.author.SetLabelText('')
            CallAfter(self.after_connect)
        else:
            debugger.addInfo('Пользователь деактивировал программу')
            api.stop_autoupdate()
            rpc.stop_autoupdate()
            self.title.SetLabelText('')
            self.author.SetLabelText('')
            self.update_icon('https://cdn.discordapp.com/attachments/1117022431748554782/1117022461045772379/logo.png')

    def exit(self):
        api.stop_autoupdate()
        rpc.stop_autoupdate()
        self.tray_icon.Destroy()
        gui.settings.Destroy()
        CallAfter(self.Destroy)

    def after_connect(self):
        self.author.SetLabelText('Подключение к api.music.yandex.ru')
        try:
            api.update()
        except Exception as e:
            self.force_disconnect(str(e))
            debugger.addError(format_exc())
            return # Если первый запрос не удался отключаемся

        self.author.SetLabelText('Подключение к Discord')
        try:
            rpc.create()
            rpc.update()
        except Exception as e:
            self.force_disconnect(str(e))
            debugger.addError(format_exc())
            return # Если не удалось обновнить статус в дискорде
        

        auto = Thread(target=api.start_autoupdate, name='YM-AutoUpdate') # Отдельный процесс для обновления данных с яндекса
        auto.start()

        auto = Thread(target=rpc.start_autoupdate, name='Discord-AutoUpdate')
        auto.start()

    def close(self, event: Event):
        self.Hide()
        self.tray_icon.ShowBalloon(f"RPC {VERSION} всё ещё работает!", "Приложение было скрыто в трей. Щёлкните по иконке что бы открыть его снова.")

    def update_icon(self, url: str):
        response = get(url)
        image_data = response.content
        img = Image.open(BytesIO(image_data))
        img.thumbnail((80, 80))
        wx_image = WxImage(img.width, img.height)
        wx_image.SetData(img.convert("RGB").tobytes())
        self.icon.SetBitmap(wx_image.ConvertToBitmap())

    def open_settings(self, event: Event):
        if not gui.settings:
            gui.settings = Settings(self)
        if gui.settings.IsIconized():
            gui.settings.Restore()
        gui.settings.SetFocus()

class TrayIcon(TaskBarIcon):
    def __init__(self, frame: Frame):
        TaskBarIcon.__init__(self)
        self.frame = frame
        self.SetIcon(Icon(LOGO), f"RPC {VERSION}")
        self.Bind(EVT_TASKBAR_LEFT_DOWN, self.onLeftClick)
        self.Bind(EVT_TASKBAR_RIGHT_DOWN, self.onRightClick)

    def CreatePopupMenu(self):
        menu = Menu()
        open_item = menu.Append(ID_ANY, "Открыть")
        self.Bind(EVT_MENU, self.onOpen, open_item)
        exit_item = menu.Append(ID_ANY, "Выход")
        self.Bind(EVT_MENU, self.onExit, exit_item)
        return menu

    def onLeftClick(self, event: Event):
        if self.frame.IsIconized():
            self.frame.Iconize(False)
        self.frame.Show(True)
        self.frame.Raise()

    def onRightClick(self, event: Event):
        self.PopupMenu(self.CreatePopupMenu())

    def onOpen(self, event: Event):
        if self.frame.IsIconized():
            self.frame.Iconize(False)
        self.frame.Show(True)
        self.frame.Raise()

    def onExit(self, event: Event):
        api.stop_autoupdate()
        rpc.stop_autoupdate()
        CallAfter(self.Destroy)
        self.frame.Destroy()