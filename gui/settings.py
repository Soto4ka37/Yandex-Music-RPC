from wx import Notebook, Panel, CheckBox, Button, RadioButton, Frame, BoxSizer, StaticText, StaticBitmap, Event, ToolTip, StaticLine, Font, SpinCtrl, Dialog, Image as WxImage, Icon
from wx import EVT_CHECKBOX, VERTICAL, ALL, EXPAND, EVT_CLOSE, ID_ANY, LI_HORIZONTAL, FONTSTYLE_NORMAL, FONTWEIGHT_NORMAL, FONTFAMILY_DEFAULT, EVT_SPINCTRL, EVT_BUTTON, HORIZONTAL, ALIGN_CENTER, EVT_RADIOBUTTON, RB_GROUP, LI_VERTICAL,  BITMAP_TYPE_ICO
from PIL import Image

def CustomIcon(frame, *, path, size, pos):
    img = Image.open(path)
    img.thumbnail(size)
    wx_image = WxImage(img.width, img.height)
    wx_image.SetData(img.convert("RGB").tobytes())
    return StaticBitmap(frame, bitmap=wx_image.ConvertToBitmap(), pos=pos)

from modules.discord import rpc
from gui.controller import gui
from modules.data import NO_ICON, NEW_ICON, OLD_ICON, LOGO, data

class YesNoDialog(Dialog):
    def __init__(self, parent, title, message):
        super(YesNoDialog, self).__init__(parent, title=title, size=(300, 110))
        self.SetIcon(Icon(LOGO)) 
        panel = Panel(self)
        vbox = BoxSizer(VERTICAL)
        
        message_label = StaticText(panel, label=message)
        vbox.Add(message_label, flag=ALL|EXPAND, border=10)
        
        buttonbox = BoxSizer(HORIZONTAL)
        yes_button = Button(panel, label='Да')
        yes_button.Bind(EVT_BUTTON, self.on_yes)
        buttonbox.Add(yes_button, flag=ALL|EXPAND, border=5)
        
        no_button = Button(panel, label='Нет')
        no_button.Bind(EVT_BUTTON, self.on_no)
        buttonbox.Add(no_button, flag=ALL|EXPAND, border=5)
        
        vbox.Add(buttonbox, flag=ALIGN_CENTER)
        
        panel.SetSizer(vbox)
        
        self.answer = None
        
    def on_yes(self, event):
        self.answer = True
        self.Close()
        
    def on_no(self, event):
        self.answer = False
        self.Close()

class Settings(Frame):
    def __init__(self, parent):
        super(Settings, self).__init__(parent, title='Настройки', size=(300, 430))
        self.SetIcon(Icon(LOGO))
        self.Bind(EVT_CLOSE, self.close)
        self.InitUI()
        self.Centre()
        self.Show()

    def close(self, evemt: Event):
        gui.settings = None
        self.Destroy()

    def InitUI(self):
        panel = Panel(self)
        notebook = Notebook(panel)
        big = Font(16, FONTFAMILY_DEFAULT, FONTSTYLE_NORMAL, FONTWEIGHT_NORMAL)

        tab1 = Panel(notebook)
        tab2 = Panel(notebook)
        tab3 = Panel(notebook)

        notebook.AddPage(tab1, "Приложение")
        notebook.AddPage(tab2, "Статус")
        notebook.AddPage(tab3, "Отладка")

        # Отладка
        StaticLine(tab3, ID_ANY, pos=(0, 0), size=(300, 1), style=LI_HORIZONTAL)

        StaticText(tab3, label='Журнал отладки', pos=(5, 3)).SetFont(big)

        StaticLine(tab3, ID_ANY, pos=(0, 30), size=(300, 1), style=LI_HORIZONTAL)
    
        button = Button(tab3, label="Открыть журнал отладки", pos=(10, 40), size=(245, 40))
        button.Bind(EVT_BUTTON, self.open_debug)


        # Приложение
        StaticLine(tab1, ID_ANY, pos=(0, 0), size=(300, 1), style=LI_HORIZONTAL)

        StaticText(tab1, label='При запуске', pos=(5, 3)).SetFont(big)

        StaticLine(tab1, ID_ANY, pos=(0, 30), size=(300, 1), style=LI_HORIZONTAL)
    
        autoconnect = CheckBox(tab1, label='Автоподключение', pos=(10, 40))
        autoconnect.SetValue(data.auto_connect)
        autoconnect.Bind(EVT_CHECKBOX, self.autoconnect_checkbox)
        
        check_updates = CheckBox(tab1, label='Проверять обновления', pos=(10, 60))
        check_updates.SetValue(data.check_updates)
        check_updates.Bind(EVT_CHECKBOX, self.checkupdates_checkbox)

        StaticLine(tab1, ID_ANY, pos=(0, 80), size=(300, 1), style=LI_HORIZONTAL)

        StaticText(tab1, label='Быстродействие', pos=(5, 83)).SetFont(big)

        StaticLine(tab1, ID_ANY, pos=(0, 110), size=(300, 1), style=LI_HORIZONTAL)
    
        check_updates = CheckBox(tab1, label='Предпросмотр трека (?)', pos=(10, 120))
        check_updates.SetValue(data.check_updates)
        check_updates.SetToolTip(ToolTip("Обновлять иконку трека в приложении (Не влияет на статус)"))
        check_updates.Bind(EVT_CHECKBOX, self.checkupdates_checkbox)

        yandex = SpinCtrl(tab1, value=str(data.yandex_request), min=1, max=30, pos=(10, 140))
        yandex.SetToolTip(ToolTip("Задержка медлу запросами в секундах (От 1 до 30)"))
        yandex.Bind(EVT_SPINCTRL, self.yandex_spin)
        StaticText(tab1, label='Задержка - music.yandex.ru', pos=(50, 144)).SetToolTip(ToolTip("Задержка между запросами в секундах (От 1 до 30)"))

        discord = SpinCtrl(tab1, value=str(data.discord_request), min=1, max=30, pos=(10, 160))
        discord.SetToolTip(ToolTip("Задержка медлу запросами в секундах (От 1 до 30)"))
        discord.Bind(EVT_SPINCTRL, self.discord_spin)
        StaticText(tab1, label='Задержка - discord.com', pos=(50, 164)).SetToolTip(ToolTip("Задержка между запросами в секундах (От 1 до 30)"))

        StaticLine(tab1, ID_ANY, pos=(0, 190), size=(300, 1), style=LI_HORIZONTAL)

        StaticText(tab1, label='Сброс', pos=(5, 193)).SetFont(big)

        StaticLine(tab1, ID_ANY, pos=(0, 220), size=(300, 1), style=LI_HORIZONTAL)

        button = Button(tab1, label="Выполнить сброс настроек", pos=(10, 230), size=(245, 40))
        button.Bind(EVT_BUTTON, self.reset)

        sizer = BoxSizer(VERTICAL)
        sizer.Add(notebook, 1, ALL|EXPAND, 5)
        panel.SetSizer(sizer)

        # Статус
        StaticLine(tab2, ID_ANY, pos=(0, 0), size=(300, 1), style=LI_HORIZONTAL)

        StaticText(tab2, label='Редакторы', pos=(5, 3)).SetFont(big)

        StaticLine(tab2, ID_ANY, pos=(0, 30), size=(300, 1), style=LI_HORIZONTAL)


        button = Button(tab2, label="Статус", pos=(10, 35), size=(116, 40))
        button.Bind(EVT_BUTTON, self.open_status_editor)

        button = Button(tab2, label="Кнопки", pos=(138, 35), size=(116, 40))
        button.Bind(EVT_BUTTON, self.open_buttons_editor)

        StaticLine(tab2, ID_ANY, pos=(0, 80), size=(300, 1), style=LI_HORIZONTAL)

        StaticText(tab2, label='Логотип', pos=(5, 83)).SetFont(big)

        StaticLine(tab2, ID_ANY, pos=(0, 110), size=(300, 1), style=LI_HORIZONTAL)

        CustomIcon(tab2, path=NO_ICON, size=(40, 40), pos=(25, 120))

        self.logo0 = RadioButton(tab2, label='Скрыть', pos=(10, 170), style=RB_GROUP)
        self.logo0.Bind(EVT_RADIOBUTTON, self.logo_choose)

        CustomIcon(tab2, path=OLD_ICON, size=(40, 120), pos=(112, 120))

        self.logo1 = RadioButton(tab2, label='Старый', pos=(102, 170))
        self.logo1.Bind(EVT_RADIOBUTTON, self.logo_choose)

        CustomIcon(tab2, path=NEW_ICON, size=(40, 200), pos=(210, 120))

        self.logo2 = RadioButton(tab2, label='Новый', pos=(200, 170))
        self.logo2.Bind(EVT_RADIOBUTTON, self.logo_choose)

        self.set_logo_default_value()

        StaticLine(tab2, ID_ANY, pos=(0, 190), size=(300, 1), style=LI_HORIZONTAL)

        StaticText(tab2, label='Таймер: Трек', pos=(5, 193)).SetFont(big)

        StaticLine(tab2, ID_ANY, pos=(0, 220), size=(300, 1), style=LI_HORIZONTAL)

        self.track_timer0 = RadioButton(tab2, label='Выключить', pos=(10, 230), style=RB_GROUP)
        self.track_timer0.Bind(EVT_RADIOBUTTON, self.track_timer)

        self.track_timer1 = RadioButton(tab2, label='Повтор (?)', pos=(10, 250))
        self.track_timer1.Bind(EVT_RADIOBUTTON, self.track_timer)
        self.track_timer1.SetToolTip(ToolTip('По завершении трека начинать таймер "Осталось" с начала'))

        StaticLine(tab2, ID_ANY, pos=(130, 223), size=(1, 45), style=LI_VERTICAL)

        self.track_timer2 = RadioButton(tab2, label='Умный (?)', pos=(145, 230))
        self.track_timer2.Bind(EVT_RADIOBUTTON, self.track_timer)
        self.track_timer2.SetToolTip(ToolTip('По завершении трека начинать заменить таймер "Осталось" на "Прошло"'))

        self.track_timer3 = RadioButton(tab2, label='Новый (?)', pos=(145, 250))
        self.track_timer3.Bind(EVT_RADIOBUTTON, self.track_timer)
        self.track_timer3.SetToolTip(ToolTip('В ожидании того, как можно будет получать текущее состояние плеера из АПИ...'))
        self.track_timer3.Disable()

        self.set_track_default_value()

        StaticLine(tab2, ID_ANY, pos=(0, 270), size=(300, 1), style=LI_HORIZONTAL)

        StaticText(tab2, label='Таймер: Поток', pos=(5, 273)).SetFont(big)

        StaticLine(tab2, ID_ANY, pos=(0, 300), size=(300, 1), style=LI_HORIZONTAL)

        self.wave_timer0 = RadioButton(tab2, label='Выключить', pos=(10, 310), style=RB_GROUP)
        self.wave_timer0.Bind(EVT_RADIOBUTTON, self.wave_timer)

        StaticLine(tab2, ID_ANY, pos=(130, 303), size=(1, 25), style=LI_VERTICAL)

        self.wave_timer1 = RadioButton(tab2, label='Прошло', pos=(145, 310))
        self.wave_timer1.Bind(EVT_RADIOBUTTON, self.wave_timer)

        self.set_wave_default_value()

    def open_debug(self, event: Event):
        pass
    def open_status_editor(self, event: Event):
        pass
    def open_buttons_editor(self, event: Event):
        pass

    def set_logo_default_value(self):
        if data.logo == 0:
            self.logo0.SetValue(True)
        elif data.logo == 1:
            self.logo1.SetValue(True)
        elif data.logo == 2:
            self.logo2.SetValue(True)

    def logo_choose(self, event: Event):
        selected = event.GetEventObject()
        if selected == self.logo0:
            data.logo = 0
        elif selected == self.logo1:
            data.logo = 1
        elif selected == self.logo2:
            data.logo = 2

        data.save()
        rpc.reload()

    def set_wave_default_value(self):
        if data.wave.timer == 0:
            self.wave_timer0.SetValue(True)
        elif data.wave.timer == 1:
            self.wave_timer1.SetValue(True)

    def wave_timer(self, event: Event):
        selected = event.GetEventObject()
        if selected == self.wave_timer0:
            data.wave.timer = 0
        elif selected == self.wave_timer1:
            data.wave.timer = 1
        data.save()
        rpc.reload()
        
    def set_track_default_value(self):
        if data.track.timer == 0:
            self.track_timer0.SetValue(True)
        elif data.track.timer == 1:
            self.track_timer1.SetValue(True)
        elif data.track.timer == 2:
            self.track_timer2.SetValue(True)
        else:
            self.track_timer3.SetValue(True)

    def track_timer(self, event: Event):
        selected = event.GetEventObject()
        if selected == self.track_timer0:
            data.track.timer = 0
        elif selected == self.track_timer1:
            data.track.timer = 1
        elif selected == self.track_timer2:
            data.track.timer = 2
        else:
            data.track.timer = 3
        data.save()
        rpc.reload()
 
    def reset (self, event: Event):
        dialog = YesNoDialog(self, 'Сброс', 'Вы действительно хотите сбросить настройки?')
        dialog.ShowModal()
        if dialog.answer:
            gui.main.force_disconnect('Сброс настроек')
            data.reset()
            gui.main.exit()

    def autoconnect_checkbox(self, event: Event):
        data.auto_connect = event.GetEventObject().GetValue()
        data.save()
        rpc.reload()
 
    def checkupdates_checkbox(self, event: Event):
        data.check_updates = event.GetEventObject().GetValue()
        data.save()
        rpc.reload()
 
    def updateicon_checkbox(self, event: Event):
        data.update_icon = event.GetEventObject().GetValue()
        data.save()
        rpc.reload()
 
    def yandex_spin(self, event: Event):
        data.yandex_request = event.GetEventObject().GetValue()
        data.save()
        rpc.reload()
 
    def discord_spin(self, event: Event):
        data.discord_request = event.GetEventObject().GetValue()
        data.save()
        rpc.reload()
 