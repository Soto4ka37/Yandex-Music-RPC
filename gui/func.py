from PIL import Image
import wx

from modules.data import LOGO

class YesNoDialog(wx.Dialog):
    def __init__(self, parent, title, message):
        super(YesNoDialog, self).__init__(parent, title=title, size=(375, 125))
        self.SetIcon(wx.Icon(LOGO))
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        message_label = wx.StaticText(panel, label=message)
        vbox.Add(message_label, flag=wx.ALL|wx.EXPAND, border=10)

        buttonbox = wx.BoxSizer(wx.HORIZONTAL)
        yes_button = wx.Button(panel, label='Да')
        yes_button.Bind(wx.EVT_BUTTON, self.on_yes)
        buttonbox.Add(yes_button, flag=wx.ALL|wx.EXPAND, border=5)

        no_button = wx.Button(panel, label='Нет')
        no_button.Bind(wx.EVT_BUTTON, self.on_no)
        buttonbox.Add(no_button, flag=wx.ALL|wx.EXPAND, border=5)

        vbox.Add(buttonbox, flag=wx.ALIGN_CENTER)

        panel.SetSizer(vbox)
        self.Centre()
        self.answer = None

    def on_yes(self, event):
        self.answer = True
        self.Destroy()

    def on_no(self, event):
        self.answer = False
        self.Destroy()


def CustomIcon(frame, *, path, size, pos):
    img = Image.open(path)
    img.thumbnail(size)
    wx_image = wx.Image(img.width, img.height)
    wx_image.SetData(img.convert('RGB').tobytes())
    return wx.StaticBitmap(frame, bitmap=wx_image.ConvertToBitmap(), pos=pos)
