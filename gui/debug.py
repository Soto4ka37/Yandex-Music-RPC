import wx 
from wx.richtext import RichTextCtrl

from re import compile, sub, DOTALL
from modules.debugger import debugger
from gui.controller import gui
from modules.data import LOGO

class DebugWindow(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, title='Журнал отладки', size=(600, 400))
        panel = wx.Panel(self)
        self.SetIcon(wx.Icon(LOGO))

        self.rtc = RichTextCtrl(panel, style=wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.TE_READONLY)

        update_button = wx.Button(panel, label='Обновить')
        update_button.Bind(wx.EVT_BUTTON, self.set_text)

        copy_button = wx.Button(panel, label='Копировать')
        copy_button.Bind(wx.EVT_BUTTON, self.on_copy)

        text_sizer = wx.BoxSizer(wx.VERTICAL)
        text_sizer.Add(self.rtc, proportion=1, flag=wx.EXPAND | wx.ALL, border=2)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.Add(copy_button, border=10)
        button_sizer.Add(update_button, border=10)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(text_sizer, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        sizer.Add(button_sizer, flag=wx.ALIGN_RIGHT | wx.ALL, border=10)

        panel.SetSizer(sizer)

        self.Bind(wx.EVT_CLOSE, self.close)
        self.set_text()
        
        self.Centre()
        self.Show()
    
    def close(self, event):
        gui.debug = None
        self.Destroy()

    def set_text(self, event = None):
        pattern = compile(r'<(inf|warn|suc|err)>(.*?)<\/\1>', DOTALL)

        debug = debugger.getStr()
        matches = pattern.findall(debug)
        self.rtc.Clear()
        
        for match in matches:
            tag, text = match
            text = sub(r'<\/?\w+>', '', text)
            if tag == 'inf':
                self.rtc.BeginTextColour(wx.BLUE)
            elif tag == 'err':
                self.rtc.BeginTextColour(wx.RED)
            elif tag == 'suc':
                self.rtc.BeginTextColour(wx.GREEN)
            else:
                self.rtc.BeginTextColour(wx.Colour(255, 128, 0))
            self.rtc.WriteText(text + '\n')
            
    def on_copy(self, event):
        self.rtc.SelectAll()
        self.rtc.Copy()