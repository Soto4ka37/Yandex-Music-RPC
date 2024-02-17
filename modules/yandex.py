from modules.data import Token
from yandex_music import Client, Track, Album, exceptions
from traceback import format_exc
from time import sleep

from modules.data import data
from modules.debugger import debugger

class CritErr(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class ShortAlbum():
    '''Упрощённый класс с информацией о альбоме'''
    def __init__(self, album: Album) -> None:
        self.name = self.title = album.title
        self.id = album.id
        self.count = album.track_count
        self.url = self.link = f"https://music.yandex.ru/album/{album.id}/"

class ShortTrack():
    '''Упрощённый класс с информацией о треке'''
    def __init__(self, track: Track):
        self.name = self.title = track.title
        self.id = track.id
        self.authors = self.artists = ', '.join(track.artists_name())
        self.icon_low = "https://" + track.cover_uri.replace("%%", "200x200")
        self.icon_high = "https://" + track.cover_uri.replace("%%", "1000x1000")
        
        self.url = self.link = f"https://music.yandex.ru/track/{track.id}/"

        self.albums = [ShortAlbum(album) for album in track.albums]
        self.album = self.albums[0]

        duration = track.duration_ms
        self.minutes = (duration // 60000)
        self.seconds = (duration // 1000) % 60

class Music:
    def __init__(self) -> None:
        self.client = self.get_yandex_client()
        self.clear()
        # По умолчанию класс имеет пустые значения, для их обновления необходимо вызвать .update()

    def clear(self):
        self.track = None
        self.last = None
        self.queue_len = None
        self.queue_index = None
        self.description = None
        self.autoupdate = None
        self.type = None

    def start_autoupdate(self):
        self.autoupdate = True
        debugger.addInfo('Автообновление запущено')
        while self.autoupdate:
            try:
                self.update()
            except:
                debugger.addWarning('Не удалось обновить трек.')
                debugger.addWarning(format_exc())
            sleep(data.yandex_request)
        self.clear()
        debugger.addInfo('Автообновление отключено; память очищена')

    def stop_autoupdate(self):
        self.autoupdate = False  

    def update(self):
        try:
            queue_list = self.client.queues_list()
            if not queue_list:
                debugger.addError('Для текущего акккаунта нет активных очередей.')
                raise CritErr('Для текущего акккаунта нет активных очередей.')
            
            queue = queue_list.pop(0).fetch_queue()
             
            self.queue_len = len(queue.tracks)
            self.queue_index = queue.current_index+1
            self.description = queue.context.description
            self.type = queue.context.type 

            # Если очередь пуста программа предплагает, что пользователь слушает поток
            if self.queue_len == 0:
                self.queue_len = '∞'
                self.track = None
                self.last = None
                return
            
            track = queue.get_current_track()

            if track.track_id == self.last:
                return
            
            self.last = track.track_id

            self.track = ShortTrack(track.fetch_track())

        except exceptions.TimedOutError:
            debugger.addWarning('TimedOut: Яндекс слишком долго на запрос.')
            self.update()
        
    def get_yandex_client(self):
        token = Token()
        try:
            client = Client(token).init()
            if not client or not client.accountStatus():
                raise CritErr('Аккаунт не валиден')
        except Exception as e:
            debugger.addError(f'Неудачная авторизация! Ошибка: {e}')
            debugger.addError(format_exc())
            token.reset()
            token.update()
            client = Client(token).init()
        debugger.addInfo(f'Успешная авторизация! Подписка на плюс {"АКТИВНА" if client.accountStatus().plus.has_plus else "НЕАКТИВНА"}.')
        return client
    

api = Music()