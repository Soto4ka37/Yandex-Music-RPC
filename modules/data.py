VERSION = 'v1.3'

import wx
import sys

from os import getenv, path, makedirs
from json import dump, load
from dotenv import dotenv_values, set_key
from requests import get

from modules.token.wx import get_token as wx_t
from modules.token.chrome import get_token as cr_t

class Warning(wx.Dialog):
    def __init__(self, parent):
        super(Warning, self).__init__(parent, title=f'Спасибо за установку YM-RPC {VERSION}', size=(400, 270))
        self.SetIcon(wx.Icon(LOGO))
        panel = wx.Panel(self)
        
        panel_sizer = wx.BoxSizer(wx.VERTICAL)
        
        text = '''Спасибо за установку Yandex Music RPC!

В данный момент API Яндекс Музыки работает нестабильно.

Статус не будет обновляться:

1) В браузерной версии по причине неизвестной ошибки на стороне Яндекса.

2) В новом клиенте по причине отсутсвии синхронизации с серверами.

Также на некоторых аккаунтах скрипт может не работать ПОЛНОСТЬЮ.'''
        static_text = wx.StaticText(panel, label=text)
        panel_sizer.Add(static_text, 0, wx.ALL, 5)

        panel_sizer.Add((0, 0), 1, wx.EXPAND)

        yes_button = wx.Button(panel, label='Перейти к авторизации')
        yes_button.Bind(wx.EVT_BUTTON, self.on_yes)
        yes_button.SetMinSize((yes_button.GetSize()[0], 40))

        panel_sizer.Add(yes_button, 0, wx.EXPAND|wx.ALL, 5)
        panel.SetSizer(panel_sizer)

        self.answer = None
        self.Centre()
        self.ShowModal()

    def on_yes(self, event):
        self.answer = True
        self.Destroy()

def download(*, url: str, path: str):
    response = get(url)
    with open(path, 'wb') as file:
        file.write(response.content)


APPDATA = getenv('APPDATA')
APP_DIR = path.join(APPDATA, 'YM-RPC-Reloaded')

LOCK_FILE = path.join(APP_DIR, 'working')
DATA_FILE = path.join(APP_DIR, 'data.json')
TOKEN_FILE = path.join(APP_DIR, 'secret.env')
LOG_FILE = path.join(APP_DIR, 'latest.log')

CACHE_DIR = path.join(APP_DIR, 'cache')

ASSETS_DIR = 'assets'

NO_ICON = path.join(ASSETS_DIR, 'no.png')
OLD_ICON = path.join(ASSETS_DIR, 'old.png')
NEW_ICON = path.join(ASSETS_DIR, 'new.png')
WAVE_ICON = path.join(ASSETS_DIR, 'wave.png')
PNG_LOGO = path.join(ASSETS_DIR, 'logo.png')
LOGO = path.join(ASSETS_DIR, 'logo.ico')

# Создание необходимых папок и скачивание необходимых файлов
if not path.exists(APP_DIR):
    makedirs(APP_DIR)

if not path.exists(CACHE_DIR):
    makedirs(CACHE_DIR)

if not path.exists(NO_ICON):
    NO_ICON = path.join(CACHE_DIR, 'no.png')
    if not path.exists(NO_ICON):
        download(url='https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC/master/assets/no.png', path=NO_ICON)

if not path.exists(OLD_ICON):
    OLD_ICON = path.join(CACHE_DIR, 'old.png')
    if not path.exists(OLD_ICON):
        download(url='https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC/master/assets/old.png', path=OLD_ICON)

if not path.exists(NEW_ICON):
    NEW_ICON = path.join(CACHE_DIR, 'new.png')
    if not path.exists(NEW_ICON):
        download(url='https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC/master/assets/new.png', path=NEW_ICON)

if not path.exists(WAVE_ICON):
    WAVE_ICON = path.join(CACHE_DIR, 'wave.png')
    if not path.exists(WAVE_ICON):
        download(url='https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC/master/assets/wave.png', path=WAVE_ICON)

if not path.exists(PNG_LOGO):
    PNG_LOGO = path.join(CACHE_DIR, 'logo.png')
    if not path.exists(PNG_LOGO):
        download(url='https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC/master/assets/logo.png', path=PNG_LOGO)

if not path.exists(LOGO):
    LOGO = path.join(CACHE_DIR, 'logo.ico')
    if not path.exists(LOGO):
        download(url='https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC/master/assets/logo.ico', path=LOGO)

if not path.exists(TOKEN_FILE):
    set_key(TOKEN_FILE, 'TOKEN', '0')

if not path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as file:
        dump({}, file)

class Token:
    def __init__(self):
        self.token = self._load()
        if not self.token or len(self.token) < 4:
            warn = Warning(None)
            if warn.answer:
                self.token = self._get_token()
                if not self.token or len(self.token) < 4:
                    sys.exit()
                else:
                    self._save()
            else:
                sys.exit()
    
    def __str__(self) -> str:
        return self.token

    def _save(self) -> None:
        set_key(TOKEN_FILE, 'TOKEN', self.token)

    def _load(self) -> str:
        config = dotenv_values(TOKEN_FILE)
        return config.get('TOKEN', None)

    def _get_token(self):
        token = wx_t()
        if not token or len(token) < 4:
            token = cr_t()
        return token

    def reset(self):
        self.token = '0'
        self._save()

    def update(self):
        self.token = self._get_token()
        self._save()

class Button:
    def __init__(self, data: dict) -> None:
        self.show_first: bool = data.get('show_first', False)
        self.label_first: str = data.get('label_first', '')
        self.url_first: str = data.get('url_first', '')
        self.show_second: bool = data.get('show_second', False)
        self.label_second: str = data.get('label_second', '')
        self.url_second: str = data.get('url_second', '')

class RPC_DATA:
    def __init__(self, data: dict) -> None:
        self.timer: int = data.get('timer', 1)
        self.details: str = data.get('details', 'Нет данных')
        self.state: str = data.get('state', '')
        self.large: str = data.get('large', 'RPC %ver% by Soto4ka37')
        self.small: str = data.get('small', 'Яндекс Музыка')
        self.button = Button(data.get('button', {}))

class Data:
    def __init__(self):
        self.load()

    def load(self):
        with open(DATA_FILE, 'r') as file:
            data: dict = load(file)
        self._load(data)

    def reset(self):
        self._load({})
        self.save()

    def _load(self, data: dict):
        self.check_updates: bool = data.get('check_updates', True)
        self.auto_connect: bool = data.get('auto_connect', True)
        self.update_icon: bool = data.get('update_icon', True)
        self.allow_cache: bool = data.get('allow_cache', True)
        self.request: int = data.get('request', 3)
        self.logo: int = data.get('logo', 2)
        self.track = RPC_DATA(data.get('track', {
            "timer": 2,
            "details": "%track-title%",
            "state": "%track-authors%",
            "large": "%album-title% (%album-len%)",
            "small": "%queue-len% из %queue-count%",
            "button": {
                "show_first": True,
                "label_first": "Слушать",
                "url_first": "%track-url%"
            }
        }))

        self.repeat = RPC_DATA(data.get('repeat', {
            "timer": 2,
            "details": "%track-title%",
            "state": "%track-authors%",
            "large": "%album-title% (%album-len%)",
            "small": "%queue-len% из %queue-count%",
            "button": {
                "show_first": True,
                "label_first": "Слушать",
                "url_first": "%track-url%"
            }
        }))

        self.wave = RPC_DATA(data.get('wave', {
            "timer": 1,
            "details": "Поток \"%description%\"",
            "state": "",
            "large": "%description%",
            "small": "Яндекс Музыка"
        }))

        self.exit_position_x = data.get('exit_position_x', None)
        self.exit_position_y = data.get('exit_position_y', None)
        self.animate_wave = data.get('animate_wave', True)

    def save(self):
        data = {
            'check_updates': self.check_updates,
            'auto_connect': self.auto_connect,
            'update_icon': self.update_icon,
            'allow_cache': self.allow_cache,
            'request': self.request,
            'exit_position_x': self.exit_position_x,
            'exit_position_y': self.exit_position_y,
            'animate_wave': self.animate_wave,
            'logo': self.logo,
            'track': {
                'timer': self.track.timer,
                'details': self.track.details,
                'state': self.track.state,
                'large': self.track.large,
                'small': self.track.small,
                'button': {
                    'show_first': self.track.button.show_first,
                    'label_first': self.track.button.label_first,
                    'url_first': self.track.button.url_first,
                    'show_second': self.track.button.show_second,
                    'label_second': self.track.button.label_second,
                    'url_second': self.track.button.url_second,
                },
            },
            'repeat': {
                'timer': 'НЕ ИСПОЛЬЗУЕТСЯ',
                'details': self.repeat.details,
                'state': self.repeat.state,
                'large': self.repeat.large,
                'small': self.repeat.small,
                'button': {
                    'show_first': self.track.button.show_first,
                    'label_first': self.track.button.label_first,
                    'url_first': self.track.button.url_first,
                    'show_second': self.track.button.show_second,
                    'label_second': self.track.button.label_second,
                    'url_second': self.track.button.url_second,
                },
            },
            'wave': {
                'timer': self.wave.timer,
                'details': self.wave.details,
                'state': self.wave.state,
                'large': self.wave.large,
                'small': self.wave.small,
                'button': {
                    'show_first': self.track.button.show_first,
                    'label_first': self.track.button.label_first,
                    'url_first': self.track.button.url_first,
                    'show_second': self.track.button.show_second,
                    'label_second': self.track.button.label_second,
                    'url_second': self.track.button.url_second,
                },
            }
        }
        with open(DATA_FILE, 'w') as file:
            dump(data, file)


data = Data()