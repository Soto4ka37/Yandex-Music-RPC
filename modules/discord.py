from pypresence import Presence
from time import time, sleep
from traceback import format_exc

from gui.controller import gui

from modules.formate import formate_string
from modules.data import data, WAVE_ICON, PNG_LOGO
from modules.yandex import api
from modules.debugger import debugger
from modules.formate import cut_string
from pypresence.exceptions import PipeClosed

from re import compile, IGNORECASE, match

def is_url(string: str):
    url_pattern = compile(
        r'^(?:http)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' 
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', IGNORECASE)
    return match(url_pattern, string) is not None

class RPC:
    def __init__(self) -> None:
        self.client = None
        self.last_description = None
        self.last_track_id = None
        self.last_timer = 0
        self.autoupdate = None
        self.now = 'clear'

        self.confirm_settings()

    def create(self):
        self.client = Presence(1116090392123822080)
        self.client.connect()

    def start_autoupdate(self):
        self.autoupdate = True
        while self.autoupdate:
            try:
                self.update()
            except PipeClosed:
                gui.main.force_disconnect('Соединение с Discord потеряно', False)
            except:
                debugger.addInfo('Не удалось обновить очередь')
                debugger.addError(format_exc())
            sleep(data.request)
        self.remove()

    def stop_autoupdate(self):
        self.autoupdate = False

    def confirm_settings(self):
        if data.logo:
            if data.logo == 2:
                self.logo = 'https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/RPC-New.png'
            else:
                self.logo = 'https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/RPC-Default.png'
        else:
            self.logo = None

        if data.track.timer == 1:
            self.repeat_func = self.track_timer1
            self.track_timer_func = self._timer_and_end
        elif data.track.timer == 2:
            self.repeat_func = self.track_timer2
            self.track_timer_func = self._timer_and_end
        else:
            self.repeat_func = self._pass_func
            self.track_timer_func = self._timer_and_end_None

        if data.wave.timer:
            self.wave_timer_func = self._timer
        else:
            self.wave_timer_func = self._timer_and_end_None

        self.track_buttons = []
        if data.track.button.show_first:
            if is_url(data.track.button.url_first) or data.track.button.url_first == '%track-url%' and data.track.button.label_first:
                self.track_buttons.append({'label': cut_string(data.track.button.label_first, 16), 'url': data.track.button.url_first})
            else:
                data.track.button.show_first = False
                data.track.button.label_first = 'Ошибка'
                data.track.button.url_first = 'Данные некорректны'
        if data.track.button.show_second:
            if is_url(data.track.button.url_second) or data.track.button.url_second == '%track-url%' and data.track.button.label_second:
                self.track_buttons.append({'label': cut_string(data.track.button.label_second, 16), 'url': data.track.button.url_second})
            else:
                data.track.button.show_second = False
                data.track.button.label_second = 'Ошибка'
                data.track.button.url_second = 'Данные некорректны'
        if not self.track_buttons:
            self.track_buttons = None

        self.repeat_buttons = []
        if data.repeat.button.show_first:
            if is_url(data.repeat.button.url_first) or data.repeat.button.url_first == '%track-url%' and data.repeat.button.label_first:
                self.repeat_buttons.append({'label': cut_string(data.repeat.button.label_first, 16), 'url': data.repeat.button.url_first})
            else:
                data.repeat.button.show_first = False
                data.repeat.button.label_first = 'Ошибка'
                data.repeat.button.url_first = 'Данные некорректны'
        if data.repeat.button.show_second:
            if is_url(data.repeat.button.url_second) or data.repeat.button.url_second == '%track-url%' and data.repeat.button.label_second:
                self.repeat_buttons.append({'label': cut_string(data.repeat.button.label_second, 16), 'url': data.repeat.button.url_second})
            else:
                data.repeat.button.show_second = False
                data.repeat.button.label_second = 'Ошибка'
                data.repeat.button.url_second = 'Данные некорректны'
        if not self.repeat_buttons:
            self.repeat_buttons = None

        self.wave_buttons = []
        if data.wave.button.show_first:
            if is_url(data.wave.button.url_first) and data.wave.button.label_first:
                self.wave_buttons.append({'label': cut_string(data.wave.button.label_first, 16), 'url': data.wave.button.url_first})
            else:
                data.wave.button.show_first = False
                data.wave.button.label_first = 'Ошибка'
                data.wave.button.url_first = 'Данные некорректны'
        if data.repeat.button.show_second:
            if is_url(data.wave.button.url_second) or data.wave.button.url_second == '%track-url%' and data.wave.button.label_second:
                self.wave_buttons.append({'label': cut_string(data.wave.button.label_second, 16), 'url': data.wave.button.url_second})
            else:
                data.wave.button.show_second = False
                data.wave.button.label_second = 'Ошибка'
                data.wave.button.url_second = 'Данные некорректны'
        if not self.wave_buttons:
            self.wave_buttons = None

    def track_timer1(self):
        repeat = data.repeat
        if time() - self.last_timer >= api.track.seconds + api.track.minutes * 60:
            self.last_timer = int(time())
            end = int(time() + api.track.minutes * 60 + api.track.seconds)
            details = formate_string(repeat.details)
            state = formate_string(repeat.state)
            large = formate_string(repeat.large)
            small = formate_string(repeat.small)
            debugger.addSuccess(f'Трек повторяется')
            
            if self.repeat_buttons:
                for button in self.repeat_buttons:
                    if button.get('url') == '%track-url%':
                        button['url'] = api.track.url

            self.client.update(
                state=state,
                details=details,
                small_image=self.logo,
                end=end,
                buttons=self.repeat_buttons,
                large_image=api.track.icon_high,
                large_text=large,
                small_text=small,
                )
            
    def track_timer2(self):
        repeat = data.repeat
        if self.now != 'r': 
            if time() - self.last_timer >= api.track.seconds + api.track.minutes * 60:
                self.now = 'r'
                details = formate_string(repeat.details)
                state = formate_string(repeat.state)
                large = formate_string(repeat.large)
                small = formate_string(repeat.small)
                debugger.addSuccess(f'Переход в режим повтора')

                if self.repeat_buttons:
                    for button in self.repeat_buttons:
                        if button.get('url') == '%track-url%':
                            button['url'] = api.track.url

                self.client.update(
                    state=state,
                    details=details,
                    small_image=self.logo,
                    start=self.last_timer,
                    buttons=self.repeat_buttons,
                    large_image=api.track.icon_high,
                    large_text=large,
                    small_text=small,
            )
                
    def _pass_func(self):
        pass

    def _timer(self):
        self.last_timer = int(time())

    def _timer_and_end(self):
        self.end = int(time() + api.track.minutes * 60 + api.track.seconds)
        self.last_timer = int(time())

    def _timer_and_end_None(self):
        self.last_timer = None
        self.end = None
    
    def update(self):
        track = data.track
        wave = data.wave
        api.update()
        if api.track: # Трек
            if self.last_track_id != api.track.id:
                self.last_track_id = api.track.id
                self.now = 't'
                self.track_timer_func()

                details = formate_string(track.details)
                state = formate_string(track.state)
                large = formate_string(track.large)
                small = formate_string(track.small)
                
                if self.track_buttons:
                    for button in self.track_buttons:
                        if button.get('url') == '%track-url%':
                            button['url'] = api.track.url

                self.client.update(
                    state=state,
                    details=details,
                    small_image=self.logo,
                    end=self.end,
                    buttons=self.track_buttons,
                    large_image=api.track.icon_high,
                    large_text=large,
                    small_text=small,
                )
                debugger.addSuccess(f'Смена трека: {details} - {state}')

                gui.main.set_title(details)
                gui.main.set_author(state)
                gui.main.set_icon(api.track.icon_low, name=f'{api.track.album.id}.png')
            else:
                self.repeat_func()

        else: # Поток
            if api.type != 'radio': # Если нет данных о треке и это не поток очищаем статус
                if self.now == 'c':
                    return
                gui.main.set_title('Нет данных')
                gui.main.set_author('')
                gui.main.set_icon(PNG_LOGO, name='logo.png')
                self.client.clear()
                self.now = 'c'
                return
            
            if self.last_description == api.description:
                return 
            
            self.last_description = api.description

            self.wave_timer_func()

            details = formate_string(wave.details)
            state = formate_string(wave.state)
            large = formate_string(wave.large)
            small = formate_string(wave.small)

            
            self.client.update(
                state=state,
                start=self.last_timer,
                details=details,
                small_image=self.logo,
                buttons=self.wave_buttons,
                large_image='https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/RPC-Wave.gif',
                large_text=large,
                small_text=small,
            )

            debugger.addSuccess(f'Смена трека: Поток - {api.description}')

            gui.main.set_title(details)
            gui.main.set_author(state)
            gui.main.set_icon(WAVE_ICON, name='wave.png')
            
    def remove(self):
        self.reload()
        if self.client:
            try: self.client.close()
            except: pass 
            self.client = None

    def reload(self):
        self.confirm_settings()
        self.now = None
        self.last_description = None
        self.last_timer = None
        self.last_track_id = None

rpc = RPC()