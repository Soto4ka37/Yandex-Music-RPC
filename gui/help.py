from wx import Frame, Panel, StaticText, Font, StaticLine, Icon
from wx import FONTFAMILY_DEFAULT, FONTSTYLE_NORMAL, FONTWEIGHT_NORMAL, ID_ANY, LI_HORIZONTAL, EVT_CLOSE, DEFAULT_FRAME_STYLE, RESIZE_BORDER, MAXIMIZE_BOX
from modules.data import LOGO
from gui.controller import gui

class Help(Frame):
    def __init__(self, parent):
        super().__init__(parent=parent, title='Список переменных', size=(340, 400), style=DEFAULT_FRAME_STYLE & ~(RESIZE_BORDER | MAXIMIZE_BOX))
        self.panel = Panel(self)
        big = Font(16, FONTFAMILY_DEFAULT, FONTSTYLE_NORMAL, FONTWEIGHT_NORMAL)

        self.Bind(EVT_CLOSE, self.close)
        self.SetIcon(Icon(LOGO))

        StaticLine(self.panel, ID_ANY, pos=(0, 0), size=(400, 1), style=LI_HORIZONTAL)

        StaticText(self.panel, label='Работают всегда', pos=(10, 3)).SetFont(big)

        StaticLine(self.panel, ID_ANY, pos=(0, 30), size=(400, 1), style=LI_HORIZONTAL)

        StaticText(self.panel, label='%ver% - Версия программы', pos=(5, 35))
        StaticText(self.panel, label='%queue-len% - Кол-во треков в очереди', pos=(5, 55))
        StaticText(self.panel, label='%queue-count% - Номер трека в очереди', pos=(5, 75))
        StaticText(self.panel, label='%description% - Название очереди (Потока)', pos=(5, 95))

        StaticLine(self.panel, ID_ANY, pos=(0, 115), size=(400, 1), style=LI_HORIZONTAL)

        StaticText(self.panel, label='Работают когда трек известен', pos=(10, 118)).SetFont(big)

        StaticLine(self.panel, ID_ANY, pos=(0, 145), size=(400, 1), style=LI_HORIZONTAL)

        StaticText(self.panel, label='%track-title% - Название трека', pos=(5, 150))
        StaticText(self.panel, label='%track-authors% - Псевдонимы авторов', pos=(5, 170))
        StaticText(self.panel, label='%track-id% - Идентификатор трека', pos=(5, 190))
        StaticText(self.panel, label='%track-url% - Ссылка на трек', pos=(5, 210))

        StaticLine(self.panel, ID_ANY, pos=(0, 230), size=(400, 1), style=LI_HORIZONTAL)

        StaticText(self.panel, label='%album-title% - Название альбома', pos=(5, 235))
        StaticText(self.panel, label='%album-len% - Кол-во треков в альбоме', pos=(5, 255))
        StaticText(self.panel, label='%album-id% - Идентификатор альбома', pos=(5, 275))
        StaticText(self.panel, label='%album-url% - Ссылка на альбом', pos=(5, 295))

        self.Centre()
        self.Show()

    def close(self):
        gui.help = None
        self.Destroy()