from modules.data import VERSION
from modules.yandex import YandexResponse

def cut_string(string: str, limit: int) -> str:
    if len(string) > limit:
        return string[:limit-2] + '..'
    else:
        return string

def edit(string: str, replace: str, to: str):
    return string.replace(replace, str(to))

def formate_string(string: str, response: YandexResponse) -> str:
    if not string:
        return None

    string = edit(string, '%ver%', str(VERSION)) # Версия программы
    string = edit(string, '%queue-len%', str(response.queue_index)) # Номер текущего трека в очереди
    string = edit(string, '%queue-count%', str(response.queue_len)) # Число треков в очереди
    string = edit(string, '%description%', str(response.description)) # Название потока
    if response.track:
        track = response.track
        album = track.album
        string = edit(string, '%track-title%', str(track.title)) # Название трека
        string = edit(string, '%track-authors%', str(track.authors)) # Авторы трека
        string = edit(string, '%track-id%', str(track.id)) # Идентификатор трека
        string = edit(string, '%track-url%', str(track.url)) # Ссылка на трек

        string = edit(string, '%album-title%', str(album.title)) # Название альбома
        string = edit(string, '%album-id%', str(album.id)) # Идентификатор трека
        string = edit(string, '%album-url%', str(album.url)) # Ссылка на альбом
        string = edit(string, '%album-len%', str(album.count)) # Количество треков в альбоме

    return cut_string(string, 96) # Лимит 96 символов