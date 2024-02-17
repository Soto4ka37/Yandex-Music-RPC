from pypresence import Presence

from gui.controller import gui
from modules.formate import formate_string
from time import time, sleep
from modules.data import data
from modules.yandex import api
class RPC:
    def __init__(self) -> None:
        self.client = None
        self.last_description = None
        self.last_track_id = None
        self.last_timer = 0
        self.autoupdate = None
        self.now = 'clear'

    def create(self):
        self.client = Presence(1116090392123822080)
        self.client.connect()

    def start_autoupdate(self):
        self.autoupdate = True
        while self.autoupdate:
            try:
                self.update()
            except:
                pass
            sleep(data.discord_request)
        self.remove()

    def stop_autoupdate(self):
        self.autoupdate = False

    def update(self):
        track = data.track
        wave = data.wave
        repeat = data.repeat

        if data.logo == 0:
            logo = None
        elif data.logo == 1:
            logo = 'https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/RPC-Default.png'
        else:
            logo = 'https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/RPC-New.png'

        if not api.track and api.type != 'radio': # При неправильных данных стираем статус
            if self.now == 'clear':
                return
            gui.main.title.SetLabelText('Неизвестно')
            gui.main.author.SetLabelText('')
            self.client.clear()
            
         
        elif not api.track: # Поток
            if self.last_description == api.description:
                return 
            self.last_description = api.description
            self.last_timer = None
            if wave.timer == 1:
                self.last_timer = int(time())

            details = formate_string(wave.details)
            state = formate_string(wave.state)
            large = formate_string(wave.large)
            small = formate_string(wave.small)

            self.client.update(
                state=state,
                start=self.last_timer,
                details=details,
                small_image=logo,
                large_image='https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/RPC-Wave.gif',
                large_text=large,
                small_text=small,
            )
            if not details:
                details = ''
            if not state:
                state = ''

            gui.main.title.SetLabelText(details)
            gui.main.author.SetLabelText(state)
            gui.main.update_icon('https://cdn.discordapp.com/attachments/1117022431748554782/1117022461045772379/logo.png')

        else:
            if self.last_track_id == api.track.id:
                if self.now == 'track' and data.track.timer != 0:
                    #print(f'{int(time() - self.last_timer)}/{api.track.seconds + api.track.minutes * 60}')
                    if time() - self.last_timer >= api.track.seconds + api.track.minutes * 60:
                        if data.track.timer == 2:
                            self.now = 'repeat'
                            details = formate_string(repeat.details)
                            state = formate_string(repeat.state)
                            large = formate_string(repeat.large)
                            small = formate_string(repeat.small)

                            self.client.update(
                                state=state,
                                details=details,
                                small_image=logo,
                                start=self.last_timer,
                                large_image=api.track.icon_high,
                                large_text=large,
                                small_text=small,
                            )

                        elif data.track.timer == 1:
                            self.last_timer = int(time())
                            end = int(time() + api.track.minutes * 60 + api.track.seconds)
                            details = formate_string(repeat.details)
                            state = formate_string(repeat.state)
                            large = formate_string(repeat.large)
                            small = formate_string(repeat.small)
                            
                            self.client.update(
                                state=state,
                                details=details,
                                small_image=logo,
                                end=end,
                                large_image=api.track.icon_high,
                                large_text=large,
                                small_text=small,
                            )
                return
            
            self.now = 'track'
            self.last_track_id = api.track.id
            self.last_timer = None
            end = None
            if track.timer == 1 or track.timer == 2:
                end = int(time() + api.track.minutes * 60 + api.track.seconds)
                self.last_timer = int(time())

            details = formate_string(track.details)
            state = formate_string(track.state)
            large = formate_string(track.large)
            small = formate_string(track.small)
            
            self.client.update(
                state=state,
                details=details,
                small_image=logo,
                end=end,
                large_image=api.track.icon_high,
                large_text=large,
                small_text=small,
            )
            if not details:
                details = ''
            if not state:
                state = ''

            gui.main.title.SetLabelText(details)
            gui.main.author.SetLabelText(state)
            gui.main.update_icon(api.track.icon_low)
            
    def remove(self):
        self.reload()
        if self.client:
            try: self.client.close()
            except: pass 
            self.client = None

    def reload(self):
        self.now = None
        self.last_description = None
        self.last_timer = None
        self.last_track_id = None

rpc = RPC()