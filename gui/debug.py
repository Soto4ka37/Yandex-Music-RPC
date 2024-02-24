from wx import Panel, Frame, VSCROLL, HSCROLL, NO_BORDER, TE_READONLY, Colour, BLUE, GREEN, RED, Button, EVT_BUTTON, VERTICAL, EXPAND, ALL, ALIGN_RIGHT, BoxSizer, EVT_CLOSE, HORIZONTAL, Icon
from wx.richtext import RichTextCtrl

from re import compile, sub, DOTALL
from modules.debugger import debugger
from gui.controller import gui
from modules.data import LOGO

class DebugWindow(Frame):
    def __init__(self, parent):
        super().__init__(parent, title='Журнал отладки', size=(600, 400))
        panel = Panel(self)
        self.SetIcon(Icon(LOGO))

        self.rtc = RichTextCtrl(panel, style=VSCROLL|HSCROLL|NO_BORDER|TE_READONLY)

        update_button = Button(panel, label='Обновить')
        update_button.Bind(EVT_BUTTON, self.set_text)

        copy_button = Button(panel, label='Копировать')
        copy_button.Bind(EVT_BUTTON, self.on_copy)

        text_sizer = BoxSizer(VERTICAL)
        text_sizer.Add(self.rtc, proportion=1, flag=EXPAND | ALL, border=2)

        button_sizer = BoxSizer(HORIZONTAL)
        button_sizer.Add(copy_button, border=10)
        button_sizer.Add(update_button, border=10)

        sizer = BoxSizer(VERTICAL)
        sizer.Add(text_sizer, proportion=1, flag=EXPAND | ALL, border=10)
        sizer.Add(button_sizer, flag=ALIGN_RIGHT | ALL, border=10)

        panel.SetSizer(sizer)

        self.Bind(EVT_CLOSE, self.close)
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
                self.rtc.BeginTextColour(BLUE)
            elif tag == 'err':
                self.rtc.BeginTextColour(RED)
            elif tag == 'suc':
                self.rtc.BeginTextColour(GREEN)
            else:
                self.rtc.BeginTextColour(Colour(255, 128, 0))
            self.rtc.WriteText(text + '\n')
            
    def on_copy(self, event):
        self.rtc.SelectAll()
        self.rtc.Copy()