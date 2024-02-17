from datetime import datetime

def current_time_formatted() -> str:
    now = datetime.now()
    formatted_time = now.strftime("%d.%m - %H:%M")
    return formatted_time

class Debugger:
    def __init__(self) -> None:
        self.debug = []

    def __str__(self) -> str:
        return self.getStr()
    
    def getStr(self):
        return '\n'.join(self.debug) + '\n'
    
    
    def addError(self, message: str):
        self.debug.append(f'<err>[{current_time_formatted()}] {message}</err>')
    
    def addInfo(self, message: str):
        self.debug.append(f'<inf>[{current_time_formatted()}] {message}</inf>')
    
    def addWarning(self, message: str):
        self.debug.append(f'<warn>[{current_time_formatted()}] {message}</warn>')
    
    def addSuccess(self, message: str):
        self.debug.append(f'<suc>[{current_time_formatted()}] {message}</suc>')
    
debugger = Debugger()