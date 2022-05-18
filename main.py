import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from utils import AppSetting
from custom_widgets import ScrollableFrame, ColorButton, Dropdown, SizeEntry
from output_pane import OutputPane
import timer

DEBUG_FLAG = True

class CountdownTimer:
    def __init__(self):
        self.root = self.init_root()

        timer.target = {
            'time': {'hh':tk.StringVar(value='01'), 'mm':tk.StringVar(value='00')},
            'duration': {'hh':tk.StringVar(value='00'), 'mm':tk.StringVar(value='00')}
        }

        self.setting = AppSetting.load()
        for key in self.setting:
            if isinstance(self.setting[key], tk.StringVar):
                self.setting[key].trace('w', lambda *args: self.output.apply_output_config())
        
        self.output = None
        self.init_widgets()

        self.root.mainloop()

    def init_root(self):
        def onExit():
            AppSetting.save(self.setting)
            self.root.destroy()
            exit()

        root = tk.Tk()
        # self.root.iconbitmap(default='icon.ico')
        root.wm_title('Countdown Timer')
        root.geometry('600x400')
        root.protocol("WM_DELETE_WINDOW", onExit)
        sf = ScrollableFrame(root, hscroll=True, vscroll=True)
        sf.pack(fill="both", expand=True)
        root = sf

        default_font = tkFont.nametofont('TkDefaultFont')
        default_font.configure(size=10)
        root.option_add('*Font', default_font)

        return root

    def init_widgets(self):
        #? preview frame
        # color frame
        display_frame = tk.Frame(self.root)
        ColorButton(display_frame, title='Background', variable=self.setting['bg']).pack(side='left', padx=(0,15))
        ColorButton(display_frame, title='Timer Text', variable=self.setting['fg']).pack(side='left', padx=15)
        tk.Label(display_frame, text='Size').pack(side='left', padx=(15,0))
        SizeEntry(display_frame, var=self.setting['size'], width=5).pack(side='left')
        display_frame.grid(row=1, column=0, columnspan=2, sticky='w', padx=(10,), pady=5)

        # set time frame
        time_frame = tk.Frame(self.root)
        def set_time(frame, var, btn_text, command):
            frame = tk.Frame(frame, highlightbackground='black', highlightthickness=1)
            Dropdown(frame, title='hour', textvariable=var['hh'], width=5, options=[f'{i:02}' for i in range(0,24)]).grid(row=0, column=0, padx=(10,5), pady=(0,10))
            Dropdown(frame, title='minute', textvariable=var['mm'], width=5, options=[f'{i:02}' for i in range(0,60,5)]).grid(row=0, column=1, padx=5, pady=(0,10))
            tk.Button(frame, text=btn_text, command=command).grid(row=0, column=2, padx=(5,10))
            return frame
        set_time(time_frame, timer.target['time'], btn_text='Set Time', command=lambda: timer.set_time()).pack(side='top', fill='both', pady=5, padx=10)
        set_time(time_frame, timer.target['duration'], btn_text='Set Duration', command=lambda: timer.set_duration()).pack(side='bottom', fill='both', pady=5, padx=10)
        time_frame.grid(row=2, column=0, sticky='n')

        # misc setting
        misc_frame = tk.Frame(self.root)
        tk.Button(misc_frame, text='10:45AM', command=lambda: timer.set_time(10, 45)).grid(row=0, column=0, sticky='w', padx=5)
        tk.Button(misc_frame, text='+15 sec', command=lambda: timer.add_duration(ss=15)).grid(row=0, column=1, sticky='w', padx=5)
        tk.Checkbutton(misc_frame, text='Show Clock', variable=self.setting['show-clock']).grid(row=1, column=0, columnspan=2, sticky='w', pady=5)
        tk.Checkbutton(misc_frame, text='Show Timer', variable=self.setting['show-timer']).grid(row=2, column=0, columnspan=2, sticky='w')
        misc_frame.grid(row=2, column=1, sticky='n', pady=5)
        
        # title, font etc
        title_frame = tk.Frame(self.root)
        tk.Label(title_frame, text='Title').grid(row=0, column=0, sticky='w')
        vcmd = (title_frame.register(lambda: True))
        ttk.Entry(title_frame, textvariable=self.setting['title'], validate='key', validatecommand=vcmd).grid(row=1, column=0, sticky='we')
        
        fonts = ['Arial', 'Calibri', 'Century', 'Comic Sans MS', 'Courier', 'Courier New', 'FangSong', 'Helvetica', 'KaiTi', 'SimHei', 'SimSun', 'Times New Roman', 'Verdana', 'Yu Gothic']
        dd_font = Dropdown(title_frame, title='Font', textvariable=self.setting['font'], options=fonts)
        dd_font.grid(row=2, column=0)
        dd_font.title.config(anchor='w')
        dd_font.title.pack(fill='x')
        title_frame.grid(row=3, column=0, sticky='wn', padx=10)

        self.output = OutputPane(self.root, self.setting)
        self.output.grid(row=1, column=2, rowspan=4, pady=(5,0))


if __name__ == "__main__":
    import ctypes
    #==========================
    # https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-messageboxw
    MB_OK = 0x0
    MB_OKCXL = 0x01
    MB_YESNOCXL = 0x03
    MB_YESNO = 0x04
    MB_HELP = 0x4000
    ICON_WARN=0x30
    ICON_INFO = 0x40
    ICON_ERROR = 0x10
    #==========================
    #==========================
    # https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-showwindow
    SW_HIDE = 0
    SW_NORMAL = 1
    SW_MAXIMIZE = 3
    SW_MINIMIZE = 6
    #==========================
    try:
        if not DEBUG_FLAG:
            # hide console window
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), SW_HIDE)
        CountdownTimer()
    except Exception as e:
        title = 'Error'
        text = str(e)
        ctypes.windll.user32.MessageBoxW(0, text, title, MB_OK | ICON_ERROR)
  
