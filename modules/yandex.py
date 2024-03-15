from yandex_music import Client, Track, Album, exceptions, QueueItem
from traceback import format_exc

from modules.data import Token
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
        self.url = self.link = f'https://music.yandex.ru/album/{album.id}/'

class ShortTrack():
    '''Упрощённый класс с информацией о треке'''
    def __init__(self, track: Track) -> None:
        self.name = self.title = track.title
        self.id = track.id
        self.authors = self.artists = ', '.join(track.artists_name())
        self.icon_low = 'https://' + track.cover_uri.replace('%%', '200x200')
        self.icon_high = 'https://' + track.cover_uri.replace('%%', '1000x1000')

        self.url = self.link = f'https://music.yandex.ru/track/{track.id}/'

        self.albums = [ShortAlbum(album) for album in track.albums]
        self.album = self.albums[0]

        duration = track.duration_ms
        self.minutes = (duration // 60000)
        self.seconds = (duration // 1000) % 60

class YandexResponse:
    def __init__(self, queue_item: QueueItem) -> None:
        self.description = queue_item.context.description
        self.type = queue_item.context.type
        if self.type == 'radio':
            self.queue_index = 0
            self.queue_len = '∞'
            self.track = None
            self.last = None
            return
        queue = queue_item.fetch_queue()

        self.queue_index = queue.current_index+1
        self.queue_len = len(queue.tracks)

        track = queue.get_current_track()

        self.last = track.track_id
        self.track = ShortTrack(track.fetch_track())

class ApiClient:
    def __init__(self) -> None:
        self.last = None
        self.client = self.get_yandex_client()

    def update(self):
        try:
            queue_list = self.client.queues_list()
            if not queue_list:
                debugger.addInfo('Для текущего акккаунта нет активных очередей.')
                raise CritErr('Для текущего акккаунта нет активных очередей.')

            queue_item = queue_list.pop(0)

            if not queue_item:
                debugger.addWarning('Не удалось получить очередь.')
                return None

        except exceptions.TimedOutError:
            debugger.addWarning('TimedOut: Яндекс слишком долго на запрос.')
            return None

        except exceptions.NotFoundError:
            debugger.addWarning('NotFound: Яндекс вернул код 404')
            return None

        return YandexResponse(queue_item=queue_item)

    def get_yandex_client(self):
        token = Token()
        try:
            client = Client(token).init()
            if not client or not client.accountStatus():
                raise CritErr('Аккаунт не валиден')
        except Exception as e:
            debugger.addInfo(f'Неудачная авторизация! Ошибка: {e}')
            debugger.addError(format_exc())
            token.reset()
            token.update()
            client = Client(token).init()
        debugger.addInfo(f'Успешная авторизация! Подписка на плюс {"АКТИВНА" if client.accountStatus().plus.has_plus else "НЕАКТИВНА"}.')
        return client


api2 = ApiClient()