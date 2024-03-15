import wx

from modules.discord import rpc
from modules.data import LOGO, data

from gui.func import YesNoDialog
from gui.controller import gui
from gui.debug import DebugWindow
from gui.status_editor import StatusEditor
from gui.buttons_editor import ButtonEditor

class Settings(wx.Frame):
    def __init__(self, parent):
        super(Settings, self).__init__(parent, title='Настройки', size=(300, 430), style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.SetIcon(wx.Icon(LOGO))
        self.Bind(wx.EVT_CLOSE, self.close)
        panel = wx.Panel(self)
        notebook = wx.Notebook(panel)
        big = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        medium = wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)

        tab1 = wx.Panel(notebook)
        tab2 = wx.Panel(notebook)
        tab3 = wx.Panel(notebook)

        notebook.AddPage(tab1, 'Приложение')
        notebook.AddPage(tab2, 'Статус')
        notebook.AddPage(tab3, 'Отладка')

        # Отладка
        wx.StaticLine(tab3, wx.ID_ANY, pos=(0, 0), size=(300, 1), style=wx.LI_HORIZONTAL)

        wx.StaticText(tab3, label='Журнал отладки', pos=(5, 3)).SetFont(big)

        wx.StaticLine(tab3, wx.ID_ANY, pos=(0, 30), size=(300, 1), style=wx.LI_HORIZONTAL)

        button = wx.Button(tab3, label='Открыть журнал отладки', pos=(10, 40), size=(245, 40))
        button.Bind(wx.EVT_BUTTON, self.open_debug)

        # Приложение
        wx.StaticLine(tab1, wx.ID_ANY, pos=(0, 0), size=(300, 1), style=wx.LI_HORIZONTAL)

        wx.StaticText(tab1, label='При запуске', pos=(5, 3)).SetFont(big)

        wx.StaticLine(tab1, wx.ID_ANY, pos=(0, 30), size=(300, 1), style=wx.LI_HORIZONTAL)

        check_updates = wx.CheckBox(tab1, label='- Проверять обновления', pos=(10, 40))
        check_updates.SetValue(data.check_updates)
        check_updates.Bind(wx.EVT_CHECKBOX, self.checkupdates_checkbox)

        autoconnect = wx.CheckBox(tab1, label='- Автоподключение', pos=(10, 60))
        autoconnect.SetValue(data.auto_connect)
        autoconnect.Bind(wx.EVT_CHECKBOX, self.autoconnect_checkbox)

        wx.StaticLine(tab1, wx.ID_ANY, pos=(0, 80), size=(300, 1), style=wx.LI_HORIZONTAL)

        wx.StaticText(tab1, label='Быстродействие', pos=(5, 83)).SetFont(big)

        wx.StaticLine(tab1, wx.ID_ANY, pos=(0, 110), size=(300, 1), style=wx.LI_HORIZONTAL)

        update_icon = wx.CheckBox(tab1, label='- Предпросмотр трека (?)', pos=(10, 120))
        update_icon.SetValue(data.update_icon)
        update_icon.SetToolTip(wx.ToolTip('Обновлять иконку трека в приложении (Не влияет на статус)'))
        update_icon.Bind(wx.EVT_CHECKBOX, self.updateicon_checkbox)

        self.allow_cache = wx.CheckBox(tab1, label='- Разрешить кэш (?)', pos=(20, 140))
        self.allow_cache.SetValue(data.allow_cache)
        self.allow_cache.SetToolTip(wx.ToolTip('Сохраняет иконки в постоянной памяти для более быстрого обновления'))
        self.allow_cache.Bind(wx.EVT_CHECKBOX, self.allowcache_checkbox)

        if not data.update_icon:
            self.allow_cache.Disable()

        discord = wx.SpinCtrl(tab1, value=str(data.request), min=1, max=10, pos=(10, 160))
        discord.SetToolTip(wx.ToolTip('Время в секундах от 1 до 10'))
        discord.Bind(wx.EVT_SPINCTRL, self.request_spin)
        wx.StaticText(tab1, label='Задержка между запросами', pos=(50, 164)).SetToolTip(wx.ToolTip('Задержка между запросами в секундах (От 1 до 10)'))

        wx.StaticLine(tab1, wx.ID_ANY, pos=(0, 190), size=(300, 1), style=wx.LI_HORIZONTAL)

        wx.StaticText(tab1, label='Сброс', pos=(5, 193)).SetFont(big)

        wx.StaticLine(tab1, wx.ID_ANY, pos=(0, 220), size=(300, 1), style=wx.LI_HORIZONTAL)

        button = wx.Button(tab1, label='Выполнить сброс настроек', pos=(5, 230), size=(255, 40))
        button.Bind(wx.EVT_BUTTON, self.reset)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.ALL|wx.EXPAND, 5)
        panel.SetSizer(sizer)

        # Статус
        wx.StaticLine(tab2, wx.ID_ANY, pos=(0, 0), size=(300, 1), style=wx.LI_HORIZONTAL)

        wx.StaticText(tab2, label='Редакторы', pos=(5, 3)).SetFont(big)

        wx.StaticLine(tab2, wx.ID_ANY, pos=(0, 30), size=(300, 1), style=wx.LI_HORIZONTAL)

        button = wx.Button(tab2, label='Статус', pos=(5, 35), size=(125, 40))
        button.Bind(wx.EVT_BUTTON, self.open_status_editor)

        button = wx.Button(tab2, label='Кнопки', pos=(135, 35), size=(125, 40))
        button.Bind(wx.EVT_BUTTON, self.open_buttons_editor)

        # - Трек

        wx.StaticLine(tab2, wx.ID_ANY, pos=(0, 80), size=(300, 1), style=wx.LI_HORIZONTAL)

        wx.StaticText(tab2, label='Трек', pos=(5, 83)).SetFont(big)

        wx.StaticLine(tab2, wx.ID_ANY, pos=(0, 110), size=(300, 1), style=wx.LI_HORIZONTAL)

        wx.StaticText(tab2, label='- Таймер', pos=(10, 113)).SetFont(medium)

        wx.StaticLine(tab2, wx.ID_ANY, pos=(0, 135), size=(300, 1), style=wx.LI_HORIZONTAL)

        self.track_timer0 = wx.RadioButton(tab2, label='Выключить', pos=(10, 140), style=wx.RB_GROUP)
        self.track_timer0.Bind(wx.EVT_RADIOBUTTON, self.track_timer)

        self.track_timer1 = wx.RadioButton(tab2, label='Повтор (?)', pos=(10, 160))
        self.track_timer1.Bind(wx.EVT_RADIOBUTTON, self.track_timer)
        self.track_timer1.SetToolTip(wx.ToolTip('По завершении трека начинать таймер "Осталось" с начала'))

        wx.StaticLine(tab2, wx.ID_ANY, pos=(130, 138), size=(1, 42), style=wx.LI_VERTICAL)

        self.track_timer2 = wx.RadioButton(tab2, label='Умный (?)', pos=(145, 140))
        self.track_timer2.Bind(wx.EVT_RADIOBUTTON, self.track_timer)
        self.track_timer2.SetToolTip(wx.ToolTip('По завершении трека начинать заменить таймер "Осталось" на "Прошло"'))

        self.track_timer3 = wx.RadioButton(tab2, label='Недоступно', pos=(145, 160))
        self.track_timer3.Bind(wx.EVT_RADIOBUTTON, self.track_timer)
        self.track_timer3.SetToolTip(wx.ToolTip('В ожидании того, как можно будет получать текущее состояние плеера из АПИ...'))
        self.track_timer3.Disable()

        self.set_track_default_value()
        # - Поток
        wx.StaticLine(tab2, wx.ID_ANY, pos=(0, 180), size=(300, 1), style=wx.LI_HORIZONTAL)

        wx.StaticText(tab2, label='Поток', pos=(5, 183)).SetFont(big)

        wx.StaticLine(tab2, wx.ID_ANY, pos=(0, 210), size=(300, 1), style=wx.LI_HORIZONTAL)

        wx.StaticText(tab2, label='- Основное', pos=(10, 213)).SetFont(medium)

        wx.StaticLine(tab2, wx.ID_ANY, pos=(0, 235), size=(300, 1), style=wx.LI_HORIZONTAL)

        self.animate_wave = wx.CheckBox(tab2, pos=(10, 240), label='Анимированная иконка (?)')
        self.animate_wave.SetToolTip(wx.ToolTip('Заменяет статичную (PNG) картинку потока на анимированную (GIF)'))
        self.animate_wave.SetValue(data.animate_wave)
        self.animate_wave.Bind(wx.EVT_CHECKBOX, self.animate_wave_checkbox)

        wx.StaticLine(tab2, wx.ID_ANY, pos=(0, 260), size=(300, 1), style=wx.LI_HORIZONTAL)

        wx.StaticText(tab2, label='- Основное', pos=(10, 263)).SetFont(medium)

        wx.StaticLine(tab2, wx.ID_ANY, pos=(0, 290), size=(300, 1), style=wx.LI_HORIZONTAL)

        self.wave_timer0 = wx.RadioButton(tab2, label='Выключить', pos=(10, 295), style=wx.RB_GROUP)
        self.wave_timer0.Bind(wx.EVT_RADIOBUTTON, self.wave_timer)

        wx.StaticLine(tab2, wx.ID_ANY, pos=(130, 292), size=(1, 25), style=wx.LI_VERTICAL)

        self.wave_timer1 = wx.RadioButton(tab2, label='Прошло {time}', pos=(145, 295))
        self.wave_timer1.Bind(wx.EVT_RADIOBUTTON, self.wave_timer)

        self.set_wave_default_value()

        self.Centre()
        self.Show()

    def close(self, evemt: wx.Event):
        gui.settings = None
        self.Destroy()

    def open_debug(self, event: wx.Event):
        if not gui.debug:
            gui.debug = DebugWindow(self)
        if gui.debug.IsIconized():
            gui.debug.Restore()
        gui.debug.SetFocus()

    def open_status_editor(self, event: wx.Event):
        if not gui.status_editor:
            gui.status_editor = StatusEditor(self)
        if gui.status_editor.IsIconized():
            gui.status_editor.Restore()
        gui.status_editor.SetFocus()

    def open_buttons_editor(self, event: wx.Event):
        if not gui.button_editor:
            gui.button_editor = ButtonEditor(self)
        if gui.button_editor.IsIconized():
            gui.button_editor.Restore()
        gui.button_editor.SetFocus()

    def set_wave_default_value(self):
        if data.wave.timer == 0:
            self.wave_timer0.SetValue(True)
        elif data.wave.timer == 1:
            self.wave_timer1.SetValue(True)

    def wave_timer(self, event: wx.Event):
        selected = event.GetEventObject()
        if selected == self.wave_timer0:
            data.wave.timer = 0
        elif selected == self.wave_timer1:
            data.wave.timer = 1
        data.save()
        rpc.reload()

    def set_track_default_value(self):
        if data.track.timer == 0:
            self.track_timer0.SetValue(True)
        elif data.track.timer == 1:
            self.track_timer1.SetValue(True)
        elif data.track.timer == 2:
            self.track_timer2.SetValue(True)
        else:
            self.track_timer3.SetValue(True)

    def track_timer(self, event: wx.Event):
        selected = event.GetEventObject()
        if selected == self.track_timer0:
            data.track.timer = 0
        elif selected == self.track_timer1:
            data.track.timer = 1
        elif selected == self.track_timer2:
            data.track.timer = 2
        else:
            data.track.timer = 3
        data.save()
        rpc.reload()
 
    def reset(self, event: wx.Event):
        dialog = YesNoDialog(self, 'Сброс', 'Вы действительно хотите сбросить настройки?')
        dialog.ShowModal()
        if dialog.answer:
            gui.main.force_disconnect('Сброс настроек', False)
            data.reset()
            gui.main.exit()

    def animate_wave_checkbox(self, event: wx.Event):
        data.animate_wave = event.GetEventObject().GetValue()
        data.save()
        rpc.reload()

    def autoconnect_checkbox(self, event: wx.Event):
        data.auto_connect = event.GetEventObject().GetValue()
        data.save()
        rpc.reload()
 
    def checkupdates_checkbox(self, event: wx.Event):
        data.check_updates = event.GetEventObject().GetValue()
        data.save()
        rpc.reload()
 
    def updateicon_checkbox(self, event: wx.Event):
        data.update_icon = event.GetEventObject().GetValue()
        if data.update_icon:
            self.allow_cache.Enable()
        else:
            self.allow_cache.Disable()
        data.save()

    def allowcache_checkbox(self, event: wx.Event):
        data.allow_cache = event.GetEventObject().GetValue()
        data.save()
 
    def request_spin(self, event: wx.Event):
        data.request = event.GetEventObject().GetValue()
        data.save()
        rpc.reload() 