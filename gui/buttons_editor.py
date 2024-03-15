import wx

from modules.data import data, LOGO
from modules.discord import rpc

from gui.controller import gui
from gui.help import Help

class ButtonEditor(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent=parent, title='Редактор кнопок', size=(400, 600), style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.panel = wx.Panel(self)

        self.Bind(wx.EVT_CLOSE, self.close)
        self.SetIcon(wx.Icon(LOGO))

        big = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)

        wx.Button(self.panel, label='Список переменных', pos=(5, 5), size=(280, 35)).Bind(wx.EVT_BUTTON, self.open_list)
        wx.Button(self.panel, label='Применить', pos=(290, 5), size=(90, 35)).Bind(wx.EVT_BUTTON, self.save)

        # Трек
        wx.StaticLine(self.panel, wx.ID_ANY, pos=(0, 45), size=(400, 1), style=wx.LI_HORIZONTAL)

        wx.StaticText(self.panel, label='Трек известен', pos=(10, 48)).SetFont(big)

        wx.StaticLine(self.panel, wx.ID_ANY, pos=(0, 75), size=(400, 1), style=wx.LI_HORIZONTAL)

        button = data.track.button
        self.track_show_first = wx.CheckBox(self.panel, pos=(5, 80), label='Кнопка 1')
        self.track_show_first.Bind(wx.EVT_CHECKBOX, self.show_track_first_func)
        self.track_show_first.SetValue(button.show_first)

        self.track_show_second = wx.CheckBox(self.panel, pos=(80, 80), label='Кнопка 2')
        self.track_show_second.Bind(wx.EVT_CHECKBOX, self.show_track_second_func)
        self.track_show_second.SetValue(button.show_second)

        self.track_label_first = wx.TextCtrl(self.panel, pos=(5, 105), size=(280, 20))
        wx.StaticText(self.panel, pos=(290, 107), label='Заголовок 1')
        self.track_label_first.SetValue(button.label_first)

        self.track_url_first = wx.TextCtrl(self.panel, pos=(5, 130), size=(280, 20))
        wx.StaticText(self.panel, pos=(290, 132), label='Ссылка 1')
        self.track_url_first.SetValue(button.url_first)

        if not button.show_first:
            self.track_label_first.Disable()
            self.track_url_first.Disable()

        self.track_label_second = wx.TextCtrl(self.panel, pos=(5, 155), size=(280, 20))
        wx.StaticText(self.panel, pos=(290, 157), label='Заголовок 2')
        self.track_label_second.SetValue(button.label_second)

        self.track_url_second = wx.TextCtrl(self.panel, pos=(5, 180), size=(280, 20))
        wx.StaticText(self.panel, pos=(290, 182), label='Ссылка 2')
        self.track_url_second.SetValue(button.url_second)

        if not button.show_second:
            self.track_label_second.Disable()
            self.track_url_second.Disable()

        # Повтор
        wx.StaticLine(self.panel, wx.ID_ANY, pos=(0, 205), size=(400, 1), style=wx.LI_HORIZONTAL)

        wx.StaticText(self.panel, label='Трек повторяется', pos=(10, 208)).SetFont(big)

        wx.StaticLine(self.panel, wx.ID_ANY, pos=(0, 235), size=(400, 1), style=wx.LI_HORIZONTAL)

        button = data.repeat.button
        self.repeat_show_first = wx.CheckBox(self.panel, pos=(5, 240), label='Кнопка 1')
        self.repeat_show_first.Bind(wx.EVT_CHECKBOX, self.show_repeat_first_func)
        self.repeat_show_first.SetValue(button.show_first)

        self.repeat_show_second = wx.CheckBox(self.panel, pos=(80, 240), label='Кнопка 2')
        self.repeat_show_second.Bind(wx.EVT_CHECKBOX, self.show_repeat_second_func)
        self.repeat_show_second.SetValue(button.show_second)

        self.repeat_label_first = wx.TextCtrl(self.panel, pos=(5, 265), size=(280, 20))
        wx.StaticText(self.panel, pos=(290, 267), label='Заголовок 1')
        self.repeat_label_first.SetValue(button.label_first)

        self.repeat_url_first = wx.TextCtrl(self.panel, pos=(5, 290), size=(280, 20))
        wx.StaticText(self.panel, pos=(290, 295), label='Ссылка 1')
        self.repeat_url_first.SetValue(button.url_first)

        if not button.show_first:
            self.repeat_label_first.Disable()
            self.repeat_url_first.Disable()

        self.repeat_label_second = wx.TextCtrl(self.panel, pos=(5, 315), size=(280, 20))
        wx.StaticText(self.panel, pos=(290, 317), label='Заголовок 2')
        self.repeat_label_second.SetValue(button.label_second)

        self.repeat_url_second = wx.TextCtrl(self.panel, pos=(5, 340), size=(280, 20))
        wx.StaticText(self.panel, pos=(290, 342), label='Ссылка 2')
        self.repeat_url_second.SetValue(button.url_second)
        
        if not button.show_second:
            self.repeat_label_second.Disable()
            self.repeat_url_second.Disable()

        # Поток
        wx.StaticLine(self.panel, wx.ID_ANY, pos=(0, 365), size=(400, 1), style=wx.LI_HORIZONTAL)

        wx.StaticText(self.panel, label='Поток', pos=(10, 368)).SetFont(big)

        wx.StaticLine(self.panel, wx.ID_ANY, pos=(0, 395), size=(400, 1), style=wx.LI_HORIZONTAL)

        button = data.wave.button
        self.wave_show_first = wx.CheckBox(self.panel, pos=(5, 400), label='Кнопка 1')
        self.wave_show_first.Bind(wx.EVT_CHECKBOX, self.show_wave_first_func)
        self.wave_show_first.SetValue(button.show_first)

        self.wave_show_second = wx.CheckBox(self.panel, pos=(80, 400), label='Кнопка 2')
        self.wave_show_second.Bind(wx.EVT_CHECKBOX, self.show_wave_second_func)
        self.wave_show_second.SetValue(button.show_second)

        self.wave_label_first = wx.TextCtrl(self.panel, pos=(5, 425), size=(280, 20))
        wx.StaticText(self.panel, pos=(290, 427), label='Заголовок 1')
        self.wave_label_first.SetValue(button.label_first)

        self.wave_url_first = wx.TextCtrl(self.panel, pos=(5, 450), size=(280, 20))
        wx.StaticText(self.panel, pos=(290, 452), label='Ссылка 1')
        self.wave_url_first.SetValue(button.url_first)

        if not button.show_first:
            self.wave_label_first.Disable()
            self.wave_url_first.Disable()

        self.wave_label_second = wx.TextCtrl(self.panel, pos=(5, 475), size=(280, 20))
        wx.StaticText(self.panel, pos=(290, 477), label='Заголовок 2')
        self.wave_label_second.SetValue(button.label_second)

        self.wave_url_second = wx.TextCtrl(self.panel, pos=(5, 500), size=(280, 20))
        wx.StaticText(self.panel, pos=(290, 502), label='Ссылка 2')
        self.wave_url_second.SetValue(button.url_second)
        
        if not button.show_second:
            self.wave_label_second.Disable()
            self.wave_url_second.Disable()

        self.Centre()
        self.Show()

    def close(self, evemt):
        gui.button_editor = None
        self.Destroy()

    def show_track_first_func(self, event):
        if self.wave_show_first.GetValue():
            self.track_label_first.Enable()
            self.track_url_first.Enable()
        else:
            self.track_label_first.Disable()
            self.track_url_first.Disable()

    def show_track_second_func(self, event):
        if self.track_show_second.GetValue():
            self.track_label_second.Enable()
            self.track_url_second.Enable()
        else:
            self.track_label_second.Disable()
            self.track_url_second.Disable()

    def show_repeat_first_func(self, event):
        if self.wave_show_first.GetValue():
            self.repeat_label_first.Enable()
            self.repeat_url_first.Enable()
        else:
            self.repeat_label_first.Disable()
            self.repeat_url_first.Disable()

    def show_repeat_second_func(self, event):
        if self.repeat_show_second.GetValue():
            self.repeat_label_second.Enable()
            self.repeat_url_second.Enable()
        else:
            self.repeat_label_second.Disable()
            self.repeat_url_second.Disable()

    def show_wave_first_func(self, event):
        if self.wave_show_first.GetValue():
            self.wave_label_first.Enable()
            self.wave_url_first.Enable()
        else:
            self.wave_label_first.Disable()
            self.wave_url_first.Disable()

    def show_wave_second_func(self, event):
        if self.wave_show_second.GetValue():
            self.wave_label_second.Enable()
            self.wave_url_second.Enable()
        else:
            self.wave_label_second.Disable()
            self.wave_url_second.Disable()
            
    def open_list(self, event):
        if not gui.help:
            gui.help = Help(self)
        if gui.help.IsIconized():
            gui.help.Restore()
        gui.help.SetFocus()
    
    def save(self, event):
        data.track.button.show_first = self.track_show_first.GetValue()
        data.track.button.label_first = self.track_label_first.GetValue()
        data.track.button.url_first = self.track_url_first.GetValue()

        data.track.button.show_second = self.track_show_second.GetValue()
        data.track.button.label_second = self.track_label_second.GetValue()
        data.track.button.url_second = self.track_url_second.GetValue()

        data.repeat.button.show_first = self.repeat_show_first.GetValue()
        data.repeat.button.label_first = self.repeat_label_first.GetValue()
        data.repeat.button.url_first = self.repeat_url_first.GetValue()

        data.repeat.button.show_second = self.repeat_show_second.GetValue()
        data.repeat.button.label_second = self.repeat_label_second.GetValue()
        data.repeat.button.url_second = self.repeat_url_second.GetValue()

        data.wave.button.show_first = self.wave_show_first.GetValue()
        data.wave.button.label_first = self.wave_label_first.GetValue()
        data.wave.button.url_first = self.wave_url_first.GetValue()

        data.wave.button.show_second = self.wave_show_second.GetValue()
        data.wave.button.label_second = self.wave_label_second.GetValue()
        data.wave.button.url_second = self.wave_url_second.GetValue()

        data.save()
        rpc.reload()

        gui.button_editor = None
        self.Destroy()