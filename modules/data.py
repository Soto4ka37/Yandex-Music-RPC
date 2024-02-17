VERSION = 'v1.0-dev-alpha'
import os
from sys import exit
from json import dump, load
from dotenv import dotenv_values, set_key
from requests import get

from modules.token.wx import get_token as wx_t
from modules.token.chrome import get_token as cr_t

def download(*, url: str, path: str):
    response = get(url)
    with open(path, 'wb') as file:
        file.write(response.content)

APPDATA = os.getenv('APPDATA')
APP_DIR = os.path.join(APPDATA, 'YM-RPC2')

LOCK_FILE = os.path.join(APP_DIR, 'working')
DATA_FILE = os.path.join(APP_DIR, 'data.json')
TOKEN_FILE = os.path.join(APP_DIR, 'secret.env')

CACHE_DIR = os.path.join(APP_DIR, 'cache')
ICONS_DIR = os.path.join(CACHE_DIR, 'icons')

NO_ICON = os.path.join(ICONS_DIR, 'no.png')
OLD_ICON = os.path.join(ICONS_DIR, 'old.png')
NEW_ICON = os.path.join(ICONS_DIR, 'new.png')

LOGO = os.path.join(ICONS_DIR, 'logo.ico')
    
if not os.path.exists(APP_DIR):
    os.makedirs(APP_DIR)

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

if not os.path.exists(ICONS_DIR):
    os.makedirs(ICONS_DIR)

if not os.path.exists(NO_ICON):
    download(url='0', path=NO_ICON)

if not os.path.exists(OLD_ICON):
    download(url='0', path=OLD_ICON)

if not os.path.exists(NEW_ICON):
    download(url='0', path=NEW_ICON)

if not os.path.exists(LOGO):
    download(url='0', path=LOGO)

if not os.path.exists(TOKEN_FILE):
    set_key(TOKEN_FILE, 'TOKEN', '0')

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as file:
       dump({}, file)

class Token:
    def __init__(self):
        self.token = self._load()
        if not self.token or len(self.token) < 4:
            self.token = self._get_token()
            if not self.token or len(self.token) < 4:
                exit()
            else:
                self._save()
                
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

class RPC_DATA:
    DEFAULTS = {
        'track': {'timer': 2, 'details': '%track-title%', 'state': '%track-authors%',
                  'large': '%album-title% (%album-count%)', 'small': 'Очередь: %queue-index%/%queue-count%'},

        'repeat': {'timer': 0, 'details': '%track-title%', 'state': '%track-authors%',
                   'large': '%album-title% (%album-count%)', 'small': 'Очередь: %queue-index%/%queue-count%'},

        'wave': {'timer': 1, 'details': 'Поток %description%', 'state': '',
                 'large': ' %description%', 'small': 'Яндекс Музык'},
    }

    def __init__(self, data: dict, rpc_type: str) -> None:
        self.type = rpc_type
        defaults = self.DEFAULTS.get(rpc_type, {})
        self.timer: int = data.get('timer', defaults.get('timer', 1))
        self.details: str = data.get('details', defaults.get('details', 'Нет данных'))
        self.state: str = data.get('state', defaults.get('state', ''))
        self.large: str = data.get('large', defaults.get('large', 'RPC %ver% by Soto4ka37'))
        self.small: str = data.get('small', defaults.get('small', 'Яндекс Музыка'))


class Data:
    def __init__(self):
        with open(DATA_FILE, "r") as file:
            data: dict = load(file)

        self.check_updates: bool = data.get('check_updates', True)
        self.auto_connect: bool = data.get('auto_connect', True)
        self.update_icon: bool = data.get('update_icon', True)
        self.yandex_request: int = data.get('yandex_request', 3)
        self.discord_request: int = data.get('discord_request', 3)
        self.logo: int = data.get('logo', 2)
        self.track = RPC_DATA(data.get('track', {}), rpc_type='track')
        self.repeat = RPC_DATA(data.get('repeat', {}), rpc_type='repeat')
        self.wave = RPC_DATA(data.get('wave', {}), rpc_type='wave')
    
    def reset(self):
        data = {}
        self.check_updates: bool = data.get('check_updates', True)
        self.auto_connect: bool = data.get('auto_connect', True)
        self.update_icon: bool = data.get('update_icon', True)
        self.yandex_request: int = data.get('yandex_request', 3)
        self.discord_request: int = data.get('discord_request', 3)
        self.logo: int = data.get('logo', 2)
        self.track = RPC_DATA(data.get('track', {}), rpc_type='track')
        self.repeat = RPC_DATA(data.get('repeat', {}), rpc_type='repeat')
        self.wave = RPC_DATA(data.get('wave', {}), rpc_type='wave')
        self.save()

    def save(self):
        data = {
            "check_updates": self.check_updates,
            "auto_connect": self.auto_connect,
            "update_icon": self.update_icon,
            "yandex_request": self.yandex_request,
            "discord_request": self.discord_request,
            "logo": self.logo,
            "track": {
                "timer": self.track.timer,
                "details": self.track.details,
                "state": self.track.state,
                "large": self.track.large,
                "small": self.track.small
            },
            "repeat": {
                "timer": 'НЕ ИСПОЛЬЗУЕТСЯ',
                "details": self.repeat.details,
                "state": self.repeat.state,
                "large": self.repeat.large,
                "small": self.repeat.small
            },
            "wave": {
                "timer": self.wave.timer,
                "details": self.wave.details,
                "state": self.wave.state,
                "large": self.wave.large,
                "small": self.wave.small
            }
        }
        with open(DATA_FILE, "w") as file:
            dump(data, file)

data = Data()