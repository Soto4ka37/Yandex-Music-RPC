import requests
import sys
from webbrowser import open as openWeb
from traceback import format_exc

from modules.debugger import debugger
from modules.data import VERSION

from gui.func import YesNoDialog

def check_versions(old: str, new: str) -> bool:
    def normalize(v):
        return [int(x) for x in v.split(".")]

    v1 = normalize(old[1:])
    v2 = normalize(new[1:])

    while len(v1) < len(v2):
        v1.append(0)
    while len(v2) < len(v1):
        v2.append(0)

    if v1 < v2:
        return True
    elif v1 > v2:
        return False
    else:
        return False

def check_updates():
    try:
        response = requests.get("https://api.github.com/repos/Soto4ka37/Yandex-Music-RPC/releases/latest", timeout=10)
        if response.status_code == 200:
            latest = response.json()
            latest_version = latest["tag_name"]
            debugger.addInfo(f'Установлена версия: {VERSION}. Последняя версия на GitHub: {latest_version}')
            print(check_versions(VERSION, latest_version))
            if check_versions(VERSION, latest_version):
                dialog = YesNoDialog(None, 'Версия устарела', f'Ваша версия ({VERSION}) устарела. Последняя версия: {latest_version}.\nЖелаете открыть GitHub?')
                dialog.ShowModal()
                if dialog.answer:
                    openWeb("https://github.com/Soto4ka37/Yandex-Music-RPC/releases/latest")
                    sys.exit()
    except Exception as e:
        debugger.addError(f'Не удалось проверить обновления! Исключение {str(e)}')
        debugger.addError(format_exc())
