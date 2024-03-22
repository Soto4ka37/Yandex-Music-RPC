from datetime import datetime
from modules.data import LOG_FILE

def current_time_formatted() -> str:
    now = datetime.now()
    formatted_time = now.strftime('%d.%m - %H:%M')
    return formatted_time

class Debugger:
    def __init__(self) -> None:
        with open(LOG_FILE, 'w', encoding='utf-8') as file:
            file.write('')

    def __str__(self) -> str:
        return self.getStr()

    def getStr(self):
        with open(LOG_FILE, 'r', encoding='utf-8') as file:
            return file.read()

    def addError(self, message: str):
        with open(LOG_FILE, 'a', encoding='utf-8') as file:
            file.write(f'<err>[{current_time_formatted()}] {message}</err>\n')

    def addInfo(self, message: str):
        with open(LOG_FILE, 'a', encoding='utf-8') as file:
            file.write(f'<inf>[{current_time_formatted()}] {message}</inf>\n')

    def addWarning(self, message: str):
        with open(LOG_FILE, 'a', encoding='utf-8') as file:
            file.write(f'<warn>[{current_time_formatted()}] {message}</warn>\n')

    def addSuccess(self, message: str):
        with open(LOG_FILE, 'a', encoding='utf-8') as file:
            file.write(f'<suc>[{current_time_formatted()}] {message}</suc>\n')


debugger = Debugger()