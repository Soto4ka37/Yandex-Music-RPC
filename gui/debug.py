import wx
from wx.richtext import RichTextCtrl

import re
from modules.debugger import debugger
from gui.controller import gui
from modules.data import LOGO

from threading import Thread

class DebugWindow(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, title='Журнал отладки', size=(600, 400))
        panel = wx.Panel(self)
        self.SetIcon(wx.Icon(LOGO))

        self.rtc = RichTextCtrl(panel, style=wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.TE_READONLY)

        self.update_button = wx.Button(panel, label='Обновить')
        self.update_button.Bind(wx.EVT_BUTTON, self.set_text)

        self.copy_button = wx.Button(panel, label='Копировать')
        self.copy_button.Bind(wx.EVT_BUTTON, self.on_copy)

        text_sizer = wx.BoxSizer(wx.VERTICAL)
        text_sizer.Add(self.rtc, proportion=1, flag=wx.EXPAND | wx.ALL, border=2)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.Add(self.copy_button, border=10)
        button_sizer.Add(self.update_button, border=10)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(text_sizer, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        sizer.Add(button_sizer, flag=wx.ALIGN_RIGHT | wx.ALL, border=10)

        panel.SetSizer(sizer)

        self.Bind(wx.EVT_CLOSE, self.close)

        self.Centre()
        self.Show()

        self.set_text()

    def close(self, event):
        gui.debug = None
        self.Destroy()

    def set_text_thread(self):
        pattern = re.compile(r'<(inf|warn|suc|err)>(.*?)<\/\1>', re.DOTALL)

        debug = debugger.getStr()
        matches = pattern.findall(debug)
        self.rtc.Clear()

        for match in matches:
            tag, text = match
            text = re.sub(r'<\/?\w+>', '', text)
            if tag == 'inf':
                self.rtc.BeginTextColour(wx.BLUE)
            elif tag == 'err':
                self.rtc.BeginTextColour(wx.RED)
            elif tag == 'suc':
                self.rtc.BeginTextColour(wx.GREEN)
            else:
                self.rtc.BeginTextColour(wx.Colour(255, 128, 0))
            self.rtc.WriteText(text + '\n')

        self.update_button.Enable()
        self.update_button.SetLabel('Обновить')

    def set_text(self, event = None):
        self.update_button.Disable()
        self.update_button.SetLabel('Обновление...')
        th = Thread(target=self.set_text_thread, name='update-text-debug')
        th.start()

    def on_copy(self, event):
        self.rtc.SelectAll()
        self.rtc.Copy()