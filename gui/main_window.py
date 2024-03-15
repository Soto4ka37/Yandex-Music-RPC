import wx
from wx.adv import TaskBarIcon, EVT_TASKBAR_LEFT_DOWN, EVT_TASKBAR_RIGHT_DOWN
from requests import get
from io import BytesIO
from PIL import Image
from threading import Thread
from traceback import format_exc
from time import sleep, time
from os import path

from gui.settings import Settings
from gui.controller import gui

from modules.debugger import debugger
from modules.data import data, VERSION, LOGO, CACHE_DIR, PNG_LOGO
from modules.yandex import api2
from modules.discord import rpc

from pypresence import exceptions as presense_exc
class MainWindow(wx.Frame):
    def __init__(self, parent = None):
        wx.Frame.__init__(self, parent, title=f'RPC {VERSION}', size=(450, 130), style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        self.dragging = None
        self.connecting = None
        self.autoudate = None
        self.last_connect = 0

        self.panel = wx.Panel(self)
        self.Bind(wx.EVT_CLOSE, self.close)

        self.tray_icon = TrayIcon(self)
        self.SetIcon(wx.Icon(LOGO))

        self.checkbox = wx.CheckBox(self.panel, label='- Активировать / Деактивировать', pos=(90, 10))
        self.checkbox.Bind(wx.EVT_CHECKBOX, self.connect)

        self.button = wx.Button(self.panel, label='Параметры', pos=(300, 8), size=(130, 20))
        self.button.Bind(wx.EVT_BUTTON, self.open_settings)

        self.line = wx.StaticLine(self.panel, wx.ID_ANY, pos=(90, 35), size=(340, 1), style=wx.LI_HORIZONTAL)

        self.title = wx.StaticText(self.panel, label='Отлючено', pos=(95, 43))
        self.author = wx.StaticText(self.panel, label='', pos=(95, 60))

        self.icon = wx.StaticBitmap(self.panel, bitmap=wx.NullBitmap, pos=(5, 5))
        self.set_icon(PNG_LOGO, name='logo.png', force=True)

        if data.exit_position_x and data.exit_position_y:
            if data.exit_position_x < 0 or data.exit_position_y < 0:
                self.Centre()
            else:
                self.SetPosition((data.exit_position_x, data.exit_position_y))
        else:
            self.Centre()

        for widget in (self.panel, self.title, self.author, self.icon, self.line):
            widget.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
            widget.Bind(wx.EVT_LEFT_UP, self.on_left_up)

        self.checkbox.SetValue(data.auto_connect)
        self.Show(True)
        if data.auto_connect:
            self.connect()

    def drag_task(self):
        click_pos = wx.GetMousePosition() - self.GetPosition()
        while self.dragging:
            self.SetPosition(wx.GetMousePosition() - click_pos)
            sleep(0.01)

    def on_left_down(self, event: wx.Event = None):
        if not self.dragging:
            self.dragging = True
            dragging = Thread(target=self.drag_task, name='Drag-Window')
            dragging.start()

    def on_left_up(self, event: wx.Event = None):
        if self.dragging:
            self.dragging = False

    def force_disconnect(self, reason: str, error: bool = True):
        rpc.stop_autoupdate()
        if reason != 'Вы переподключаетесь слишком часто!':
            self.last_connect = time()
        if error:
            self.set_title('Произошла ошибка')
            self.set_author(reason)
        else:
            self.set_title(reason)
            self.set_author('')
        self.set_icon(PNG_LOGO, name='logo.png')
        debugger.addInfo(f'Аварийное завершение: {reason}')
        self.checkbox.SetValue(False)

    def connect(self, event: wx.Event = None):
        checkbox = self.checkbox
        if self.connecting and self.connecting.is_alive():
            checkbox.SetValue(not checkbox.GetValue())
            return
        now = time()
        cooldown = now - self.last_connect
        if checkbox.GetValue():
            debugger.addInfo('Пользователь активировал программу')
            if cooldown < 10:
                self.force_disconnect('Вы переподключаетесь слишком часто!', False)
                self.set_author(f'Повторите попытку через {round(10-cooldown, 2)} сек.')
                return
            self.checkbox.Disable()
            self.set_title('Загрузка...')
            self.set_author('')
            self.connecting = Thread(target=self.after_connect, name='Connecting')
            self.connecting.start()
        else:
            debugger.addInfo('Пользователь деактивировал программу')
            self.last_connect = time()
            rpc.stop_autoupdate()
            self.set_title('Работа завершена')
            self.set_author('')
            self.set_icon(PNG_LOGO, name='logo.png')

    def after_connect(self):
        self.set_author('Подключение к api.music.yandex.ru')
        try:
            api2.update()
        except Exception as e:
            debugger.addInfo('Запрос на api.music.yandex.ru не удался')
            self.force_disconnect(str(e), True)
            debugger.addError(format_exc())
            self.checkbox.Enable()
            return # Если первый запрос не удался

        self.set_author('Подключение к Discord RPC')

        try:
            rpc.create()
        except presense_exc.DiscordNotFound:
            self.force_disconnect('Не удалось установить соединение с Discord RPC', False)
            debugger.addError(format_exc())
            self.checkbox.Enable()
            return # Если не удалось подключиться к Discord RPC

        try:
            rpc.update()
        except Exception as e:
            self.force_disconnect(str(e), True)
            debugger.addInfo('Не удалось обновить статус')
            debugger.addError(format_exc())
            self.checkbox.Enable()
            return # Если не удалось обновнить статус

        if self.autoudate and self.autoudate.is_alive():
            while self.autoudate.is_alive():
                self.set_author('Ожидание завершения предыдущего потока')
                sleep(1)

        self.autoudate = Thread(target=rpc.start_autoupdate, name='UpdateThread')
        self.autoudate.start()
        self.checkbox.Enable()

    def exit(self):
        data.exit_position_x, data.exit_position_y = self.GetPosition()
        rpc.stop_autoupdate()
        self.tray_icon.Destroy()
        if gui.settings:
            gui.settings.Destroy()
            gui.settings = None
        if gui.debug:
            gui.debug.Destroy()
            gui.debug = None
        if gui.button_editor:
            gui.button_editor.Destroy()
            gui.button_editor = None
        if gui.status_editor:
            gui.status_editor.Destroy()
            gui.status_editor = None
        if gui.help:
            gui.help.Destroy()
            gui.help = None
        wx.CallAfter(self.Destroy)

    def close(self, event: wx.Event):
        if gui.settings:
            gui.settings.Destroy()
            gui.settings = None
        if gui.debug:
            gui.debug.Destroy()
            gui.debug = None
        if gui.button_editor:
            gui.button_editor.Destroy()
            gui.button_editor = None
        if gui.status_editor:
            gui.status_editor.Destroy()
            gui.status_editor = None
        if gui.help:
            gui.help.Destroy()
            gui.help = None
        self.Hide()
        self.tray_icon.ShowBalloon(f'RPC {VERSION} всё ещё работает!', 'Приложение было скрыто в трей. Щёлкните по иконке что бы открыть его снова.')

    def set_title(self, text: str = None):
        if text:
            self.title.SetLabelText(text)
        else:
            self.title.SetLabelText('')

    def set_author(self, text: str = None):
        if text:
            self.author.SetLabelText(text)
        else:
            self.author.SetLabelText('')

    def set_icon(self, path_or_url: str, name: str, force: bool = False):
        if not data.update_icon and not force:
            return

        if 'https://' in path_or_url or 'http://' in path_or_url:
            cache_image = path.join(CACHE_DIR, name)
            if not path.exists(cache_image):
                response = get(path_or_url)
                image_data = response.content
                if data.allow_cache:
                    with open(cache_image, 'wb') as file:
                        file.write(image_data) # Кешируем картинку

                img = Image.open(BytesIO(image_data))
            else:
                img = Image.open(cache_image)
        else:
            img = Image.open(path_or_url)
        img.thumbnail((80, 80))
        wx_image = wx.Image(img.width, img.height)
        wx_image.SetData(img.convert('RGB').tobytes())
        self.icon.SetBitmap(wx_image.ConvertToBitmap())

    def open_settings(self, event: wx.Event):
        if not gui.settings:
            gui.settings = Settings(self)
        if gui.settings.IsIconized():
            gui.settings.Restore()
        gui.settings.SetFocus()

class TrayIcon(TaskBarIcon):
    def __init__(self, frame: wx.Frame):
        TaskBarIcon.__init__(self)
        self.frame = frame
        self.SetIcon(wx.Icon(LOGO), f'RPC {VERSION}')
        self.Bind(EVT_TASKBAR_LEFT_DOWN, self.onLeftClick)
        self.Bind(EVT_TASKBAR_RIGHT_DOWN, self.onRightClick)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        open_item = menu.Append(wx.ID_ANY, 'Открыть')
        self.Bind(wx.EVT_MENU, self.onOpen, open_item)
        exit_item = menu.Append(wx.ID_ANY, 'Выход')
        self.Bind(wx.EVT_MENU, self.onExit, exit_item)
        return menu

    def onLeftClick(self, event: wx.Event):
        if self.frame.IsIconized():
            self.frame.Iconize(False)
        self.frame.Show(True)
        self.frame.Raise()

    def onRightClick(self, event: wx.Event):
        self.PopupMenu(self.CreatePopupMenu())

    def onOpen(self, event: wx.Event):
        if self.frame.IsIconized():
            self.frame.Iconize(False)
        self.frame.Show(True)
        self.frame.Raise()

    def onExit(self, event: wx.Event):
        data.exit_position_x, data.exit_position_y = self.frame.GetPosition()
        rpc.stop_autoupdate()
        self.frame.Destroy()
        if gui.settings:
            gui.settings.Destroy()
            gui.settings = None
        if gui.debug:
            gui.debug.Destroy()
            gui.debug = None
        if gui.button_editor:
            gui.button_editor.Destroy()
            gui.button_editor = None
        if gui.status_editor:
            gui.status_editor.Destroy()
            gui.status_editor = None
        if gui.help:
            gui.help.Destroy()
            gui.help = None
        wx.CallAfter(self.Destroy)