import wx
from wx.html2 import WebView, EVT_WEBVIEW_NAVIGATING

class Browser(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title='Получение токена (Способ от KycTik31)', size=(450, 600))
        self.browser: WebView = WebView.New(self)
        self.browser.Bind(EVT_WEBVIEW_NAVIGATING, self.OnUrlChanged)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Centre()
        self.token = None

    def OnUrlChanged(self, event):
        url = event.GetURL()
        if '#access_token' in url:
            self.token = url.split('=')[1].split('&')[0]
            self.Destroy()

    def OnClose(self, event):
        self.Destroy()


def get_token() -> str:
    browser = Browser(None)
    browser.browser.LoadURL(
        'https://oauth.yandex.ru/authorize?response_type=token&client_id=23cabbbdc6cd418abb4b39c32c41195d')
    browser.ShowModal()
    return browser.token
