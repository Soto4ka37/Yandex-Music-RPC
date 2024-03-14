import wx
from modules.data import LOGO
from gui.controller import gui

class Help(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent=parent, title='Список переменных', size=(340, 400), style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.panel = wx.Panel(self)
        big = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)

        self.Bind(wx.EVT_CLOSE, self.close)
        self.SetIcon(wx.Icon(LOGO))

        wx.StaticLine(self.panel, wx.ID_ANY, pos=(0, 0), size=(400, 1), style=wx.LI_HORIZONTAL)

        wx.StaticText(self.panel, label='Работают всегда', pos=(10, 3)).SetFont(big)

        wx.StaticLine(self.panel, wx.ID_ANY, pos=(0, 30), size=(400, 1), style=wx.LI_HORIZONTAL)

        wx.StaticText(self.panel, label='%ver% - Версия программы', pos=(5, 35))
        wx.StaticText(self.panel, label='%queue-len% - Кол-во треков в очереди', pos=(5, 55))
        wx.StaticText(self.panel, label='%queue-count% - Номер трека в очереди', pos=(5, 75))
        wx.StaticText(self.panel, label='%description% - Название очереди (Потока)', pos=(5, 95))

        wx.StaticLine(self.panel, wx.ID_ANY, pos=(0, 115), size=(400, 1), style=wx.LI_HORIZONTAL)

        wx.StaticText(self.panel, label='Работают когда трек известен', pos=(10, 118)).SetFont(big)

        wx.StaticLine(self.panel, wx.ID_ANY, pos=(0, 145), size=(400, 1), style=wx.LI_HORIZONTAL)

        wx.StaticText(self.panel, label='%track-title% - Название трека', pos=(5, 150))
        wx.StaticText(self.panel, label='%track-authors% - Псевдонимы авторов', pos=(5, 170))
        wx.StaticText(self.panel, label='%track-id% - Идентификатор трека', pos=(5, 190))
        wx.StaticText(self.panel, label='%track-url% - Ссылка на трек', pos=(5, 210))

        wx.StaticLine(self.panel, wx.ID_ANY, pos=(0, 230), size=(400, 1), style=wx.LI_HORIZONTAL)

        wx.StaticText(self.panel, label='%album-title% - Название альбома', pos=(5, 235))
        wx.StaticText(self.panel, label='%album-len% - Кол-во треков в альбоме', pos=(5, 255))
        wx.StaticText(self.panel, label='%album-id% - Идентификатор альбома', pos=(5, 275))
        wx.StaticText(self.panel, label='%album-url% - Ссылка на альбом', pos=(5, 295))

        self.Centre()
        self.Show()

    def close(self):
        gui.help = None
        self.Destroy()