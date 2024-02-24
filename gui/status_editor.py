from wx import Frame, Panel, TextCtrl, Button, StaticText, Font, StaticLine, Icon
from wx import EVT_BUTTON, FONTFAMILY_DEFAULT, FONTSTYLE_NORMAL, FONTWEIGHT_NORMAL, ID_ANY, LI_HORIZONTAL, EVT_CLOSE, DEFAULT_FRAME_STYLE, RESIZE_BORDER, MAXIMIZE_BOX

from modules.data import data, LOGO
from gui.controller import gui
from gui.help import Help

class StatusEditor(Frame):
    def __init__(self, parent):
        super().__init__(parent=parent, title='Редактор статуса', size=(400, 500), style=DEFAULT_FRAME_STYLE & ~(RESIZE_BORDER | MAXIMIZE_BOX))
        self.panel = Panel(self)

        self.Bind(EVT_CLOSE, self.close)
        self.SetIcon(Icon(LOGO))

        big = Font(16, FONTFAMILY_DEFAULT, FONTSTYLE_NORMAL, FONTWEIGHT_NORMAL)

        Button(self.panel, label='Список переменных', pos=(5, 5), size=(280, 35)).Bind(EVT_BUTTON, self.open_list)
        Button(self.panel, label='Применить', pos=(290, 5), size=(90, 35)).Bind(EVT_BUTTON, self.save)

        # Трек
        StaticLine(self.panel, ID_ANY, pos=(0, 45), size=(400, 1), style=LI_HORIZONTAL)

        StaticText(self.panel, label='Трек известен', pos=(10, 48)).SetFont(big)

        StaticLine(self.panel, ID_ANY, pos=(0, 75), size=(400, 1), style=LI_HORIZONTAL)

        self.track_details = TextCtrl(self.panel, pos=(5, 80), size=(280, 20))
        StaticText(self.panel, pos=(290, 82), label='Верхний текст')
        self.track_details.SetValue(data.track.details)

        self.track_state = TextCtrl(self.panel, pos=(5, 105), size=(280, 20))
        StaticText(self.panel, pos=(290, 107), label='Нижний текст')
        self.track_state.SetValue(data.track.state)

        self.track_large = TextCtrl(self.panel, pos=(5, 130), size=(280, 20))
        StaticText(self.panel, pos=(290, 132), label='Картинка')
        self.track_large.SetValue(data.track.large)

        self.track_small = TextCtrl(self.panel, pos=(5, 155), size=(280, 20))
        StaticText(self.panel, pos=(290, 157), label='Логотип')
        self.track_small.SetValue(data.track.small)
        
        # Повтор
        StaticLine(self.panel, ID_ANY, pos=(0, 180), size=(400, 1), style=LI_HORIZONTAL)

        StaticText(self.panel, label='Трек повторяется', pos=(10, 183)).SetFont(big)

        StaticLine(self.panel, ID_ANY, pos=(0, 210), size=(400, 1), style=LI_HORIZONTAL)

        self.repeat_details = TextCtrl(self.panel, pos=(5, 215), size=(280, 20))
        StaticText(self.panel, pos=(290, 217), label='Верхний текст')
        self.repeat_details.SetValue(data.repeat.details)

        self.repeat_state = TextCtrl(self.panel, pos=(5, 240), size=(280, 20))
        StaticText(self.panel, pos=(290, 242), label='Нижний текст')
        self.repeat_state.SetValue(data.repeat.state)

        self.repeat_large = TextCtrl(self.panel, pos=(5, 265), size=(280, 20))
        StaticText(self.panel, pos=(290, 267), label='Картинка')
        self.repeat_large.SetValue(data.repeat.large)

        self.repeat_small = TextCtrl(self.panel, pos=(5, 290), size=(280, 20))
        StaticText(self.panel, pos=(290, 292), label='Логотип')
        self.repeat_small.SetValue(data.repeat.small)

        # Поток
        StaticLine(self.panel, ID_ANY, pos=(0, 315), size=(400, 1), style=LI_HORIZONTAL)

        StaticText(self.panel, label='Поток', pos=(10, 318)).SetFont(big)

        StaticLine(self.panel, ID_ANY, pos=(0, 345), size=(400, 1), style=LI_HORIZONTAL)

        self.wave_details = TextCtrl(self.panel, pos=(5, 350), size=(280, 20))
        StaticText(self.panel, pos=(290, 352), label='Верхний текст')
        self.wave_details.SetValue(data.wave.details)

        self.wave_state = TextCtrl(self.panel, pos=(5, 375), size=(280, 20))
        StaticText(self.panel, pos=(290, 377), label='Нижний текст')
        self.wave_state.SetValue(data.wave.state)

        self.wave_large = TextCtrl(self.panel, pos=(5, 400), size=(280, 20))
        StaticText(self.panel, pos=(290, 402), label='Картинка')
        self.wave_large.SetValue(data.wave.large)

        self.wave_small = TextCtrl(self.panel, pos=(5, 425), size=(280, 20))
        StaticText(self.panel, pos=(290, 427), label='Логотип')
        self.wave_small.SetValue(data.wave.small)

        self.Centre()
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

        gui.status_editor = None
        self.Destroy()