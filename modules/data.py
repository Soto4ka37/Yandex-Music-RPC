VERSION = '1.1-beta'

from os import getenv, path, makedirs
from json import dump, load
from dotenv import dotenv_values, set_key
from requests import get

from modules.token.wx import get_token as wx_t
from modules.token.chrome import get_token as cr_t

def download(*, url: str, path: str):
    response = get(url)
    with open(path, 'wb') as file:
        file.write(response.content)

APPDATA = getenv('APPDATA')
APP_DIR = path.join(APPDATA, 'YM-RPC-Reloaded')

# --------

LOCK_FILE = path.join(APP_DIR, 'working')
DATA_FILE = path.join(APP_DIR, 'data.json')
TOKEN_FILE = path.join(APP_DIR, 'secret.env')
LOG_FILE = path.join(APP_DIR, 'latest.log')

CACHE_DIR = path.join(APP_DIR, 'cache')

# -------- 

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
    download(url='https://www.soto4ka37.ru/file/no.png', path=NO_ICON)

if not path.exists(OLD_ICON):
    OLD_ICON = path.join(CACHE_DIR, 'old.png')
    download(url='https://www.soto4ka37.ru/file/old.png', path=OLD_ICON)

if not path.exists(NEW_ICON):
    NEW_ICON = path.join(CACHE_DIR, 'new.png')
    download(url='https://www.soto4ka37.ru/file/new.png', path=NEW_ICON)

if not path.exists(WAVE_ICON):
    WAVE_ICON = path.join(CACHE_DIR, 'wave.png')
    download(url='https://www.soto4ka37.ru/file/wave.png', path=WAVE_ICON)

if not path.exists(PNG_LOGO):
    PNG_LOGO = path.join(CACHE_DIR, 'logo.png')
    download(url='https://www.soto4ka37.ru/file/logo.png', path=PNG_LOGO)

if not path.exists(LOGO):
    LOGO = path.join(CACHE_DIR, 'logo.ico')
    download(url='https://www.soto4ka37.ru/file/logo.ico', path=LOGO)

if not path.exists(TOKEN_FILE):
    set_key(TOKEN_FILE, 'TOKEN', '0')

if not path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as file:
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
        self.track = RPC_DATA(data.get('track', {'timer': 2, 'details': '%track-title%', 'state': '%track-authors%', 'large': '%album-title% (%album-len%)', 'small': '%queue-len% из %queue-count%', 'button': {'show_first': True, 'label_first': 'Слушать', 'url_first': '%track-url%'}}))
        self.repeat = RPC_DATA(data.get('repeat', {'timer': 0, 'details': '%track-title%', 'state': '%track-authors%', 'large': '%album-title% (%album-len%)', 'small': 'Трек повторяется', 'button': {'show_first': True, 'label_first': 'Слушать', 'url_first': '%track-url%'}}))
        self.wave = RPC_DATA(data.get('wave', {'timer': 1, 'details': 'Поток "%description%"', 'state': '', 'large': ' %description%', 'small': 'Яндекс Музыка'}))
        self.exit_position_x = data.get('exit_position_x', None)
        self.exit_position_y = data.get('exit_position_y', None)

    def save(self):
        data = {
            'check_updates': self.check_updates,
            'auto_connect': self.auto_connect,
            'update_icon': self.update_icon,
            'allow_cache': self.allow_cache,
            'request': self.request,
            'exit_position_x': self.exit_position_x,
            'exit_position_y': self.exit_position_y,
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