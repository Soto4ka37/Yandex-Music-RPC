import wx

from modules.data import data, LOGO, NO_ICON, NEW_ICON, OLD_ICON
from modules.discord import rpc

from gui.func import CustomIcon
from gui.controller import gui
from gui.help import Help

class StatusEditor(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent=parent, title='Редактор статуса', size=(400, 600), style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.panel = wx.Panel(self)

        self.Bind(wx.EVT_CLOSE, self.close)
        self.SetIcon(wx.Icon(LOGO))

        big = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)

        wx.Button(self.panel, label='Список переменных', pos=(5, 5), size=(280, 35)).Bind(wx.EVT_BUTTON, self.open_list)
        wx.Button(self.panel, label='Применить', pos=(290, 5), size=(90, 35)).Bind(wx.EVT_BUTTON, self.save)

        # Логотип
        wx.StaticLine(self.panel, wx.ID_ANY, pos=(0, 45), size=(400, 1), style=wx.LI_HORIZONTAL)

        wx.StaticText(self.panel, label='Логотип', pos=(5, 48)).SetFont(big)

        wx.StaticLine(self.panel, wx.ID_ANY, pos=(0, 75), size=(400, 1), style=wx.LI_HORIZONTAL)

        CustomIcon(self.panel, path=NO_ICON, size=(40, 40), pos=(35, 85))

        self.logo0 = wx.RadioButton(self.panel, label='Скрыть', pos=(25, 130), style=wx.RB_GROUP)
        self.logo0.Bind(wx.EVT_RADIOBUTTON, self.logo_choose)

        CustomIcon(self.panel, path=OLD_ICON, size=(40, 40), pos=(165, 85))

        self.logo1 = wx.RadioButton(self.panel, label='Старый', pos=(155, 130))
        self.logo1.Bind(wx.EVT_RADIOBUTTON, self.logo_choose)

        CustomIcon(self.panel, path=NEW_ICON, size=(40, 40), pos=(300, 85))

        self.logo2 = wx.RadioButton(self.panel, label='Новый', pos=(290, 130))
        self.logo2.Bind(wx.EVT_RADIOBUTTON, self.logo_choose)

        # Трек
        wx.StaticLine(self.panel, wx.ID_ANY, pos=(0, 150), size=(400, 1), style=wx.LI_HORIZONTAL)

        wx.StaticText(self.panel, label='Трек известен', pos=(10, 153)).SetFont(big)

        wx.StaticLine(self.panel, wx.ID_ANY, pos=(0, 180), size=(400, 1), style=wx.LI_HORIZONTAL)

        self.track_details = wx.TextCtrl(self.panel, pos=(5, 185), size=(280, 20))
        wx.StaticText(self.panel, pos=(290, 187), label='Верхний текст')
        self.track_details.SetValue(data.track.details)

        self.track_state = wx.TextCtrl(self.panel, pos=(5, 205), size=(280, 20))
        wx.StaticText(self.panel, pos=(290, 207), label='Нижний текст')
        self.track_state.SetValue(data.track.state)

        self.track_large = wx.TextCtrl(self.panel, pos=(5, 230), size=(280, 20))
        wx.StaticText(self.panel, pos=(290, 232), label='Картинка')
        self.track_large.SetValue(data.track.large)

        self.track_small = wx.TextCtrl(self.panel, pos=(5, 255), size=(280, 20))
        wx.StaticText(self.panel, pos=(290, 257), label='Логотип')
        self.track_small.SetValue(data.track.small)

        # Повтор
        wx.StaticLine(self.panel, wx.ID_ANY, pos=(0, 280), size=(400, 1), style=wx.LI_HORIZONTAL)

        wx.StaticText(self.panel, label='Трек повторяется', pos=(10, 283)).SetFont(big)

        wx.StaticLine(self.panel, wx.ID_ANY, pos=(0, 310), size=(400, 1), style=wx.LI_HORIZONTAL)

        self.repeat_details = wx.TextCtrl(self.panel, pos=(5, 315), size=(280, 20))
        wx.StaticText(self.panel, pos=(290, 317), label='Верхний текст')
        self.repeat_details.SetValue(data.repeat.details)

        self.repeat_state = wx.TextCtrl(self.panel, pos=(5, 340), size=(280, 20))
        wx.StaticText(self.panel, pos=(290, 342), label='Нижний текст')
        self.repeat_state.SetValue(data.repeat.state)

        self.repeat_large = wx.TextCtrl(self.panel, pos=(5, 365), size=(280, 20))
        wx.StaticText(self.panel, pos=(290, 367), label='Картинка')
        self.repeat_large.SetValue(data.repeat.large)

        self.repeat_small = wx.TextCtrl(self.panel, pos=(5, 390), size=(280, 20))
        wx.StaticText(self.panel, pos=(290, 392), label='Логотип')
        self.repeat_small.SetValue(data.repeat.small)

        # Поток
        wx.StaticLine(self.panel, wx.ID_ANY, pos=(0, 415), size=(400, 1), style=wx.LI_HORIZONTAL)

        wx.StaticText(self.panel, label='Поток', pos=(10, 418)).SetFont(big)

        wx.StaticLine(self.panel, wx.ID_ANY, pos=(0, 445), size=(400, 1), style=wx.LI_HORIZONTAL)

        self.wave_details = wx.TextCtrl(self.panel, pos=(5, 450), size=(280, 20))
        wx.StaticText(self.panel, pos=(290, 452), label='Верхний текст')
        self.wave_details.SetValue(data.wave.details)

        self.wave_state = wx.TextCtrl(self.panel, pos=(5, 475), size=(280, 20))
        wx.StaticText(self.panel, pos=(290, 477), label='Нижний текст')
        self.wave_state.SetValue(data.wave.state)

        self.wave_large = wx.TextCtrl(self.panel, pos=(5, 500), size=(280, 20))
        wx.StaticText(self.panel, pos=(290, 502), label='Картинка')
        self.wave_large.SetValue(data.wave.large)

        self.wave_small = wx.TextCtrl(self.panel, pos=(5, 525), size=(280, 20))
        wx.StaticText(self.panel, pos=(290, 527), label='Логотип')
        self.wave_small.SetValue(data.wave.small)

        self.Centre()
        self.set_logo_default_value()
        self.Show()

    def close(self, evemt):
        gui.status_editor = None
        self.Destroy()

    def open_list(self, event):
        if not gui.help:
            gui.help = Help(self)
        if gui.help.IsIconized():
            gui.help.Restore()
        gui.help.SetFocus()

    def set_logo_default_value(self):
        if data.logo == 0:
            self.wave_small.Disable()
            self.repeat_small.Disable()
            self.track_small.Disable()
            self.logo0.SetValue(True)
        elif data.logo == 1:
            self.logo1.SetValue(True)
        elif data.logo == 2:
            self.logo2.SetValue(True)

    def logo_choose(self, event: wx.Event):
        selected = event.GetEventObject()
        if selected == self.logo0:
            data.logo = 0
            self.wave_small.Disable()
            self.repeat_small.Disable()
            self.track_small.Disable()
        elif selected == self.logo1:
            data.logo = 1
            self.wave_small.Enable()
            self.repeat_small.Enable()
            self.track_small.Enable()
        elif selected == self.logo2:
            self.wave_small.Enable()
            self.repeat_small.Enable()
            self.track_small.Enable()
            data.logo = 2

        data.save()
        rpc.reload()

    def save(self, event):
        data.track.details = self.track_details.GetValue()
        data.track.state = self.track_state.GetValue()
        data.track.large = self.track_large.GetValue()
        data.track.small = self.track_small.GetValue()

        data.repeat.details = self.repeat_details.GetValue()
        data.repeat.state = self.repeat_state.GetValue()
        data.repeat.large = self.repeat_large.GetValue()
        data.repeat.small = self.repeat_small.GetValue()

        data.wave.details = self.wave_details.GetValue()
        data.wave.state = self.wave_state.GetValue()
        data.wave.large = self.wave_large.GetValue()
        data.wave.small = self.wave_small.GetValue()

        data.save()
        rpc.reload()

        gui.status_editor = None
        self.Destroy()