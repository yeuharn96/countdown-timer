import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser

FIT_WIDTH = "fit_width"
FIT_HEIGHT = "fit_height"

### https://stackoverflow.com/questions/66213754/unable-to-scroll-frame-using-mouse-wheel-adding-horizontal-scrollbar/66215091#66215091
class ScrollableFrame(tk.Frame):
    """
    There is no way to scroll <tkinter.Frame> so we are
    going to create a canvas and place the frame there.
    Scrolling the canvas will give the illusion of scrolling
    the frame
    Partly taken from:
        https://blog.tecladocode.com/tkinter-scrollable-frames/
        https://stackoverflow.com/a/17457843/11106801
    master_frame---------------------------------------------------------
    | dummy_canvas-----------------------------------------  y_scroll--  |
    | | self---------------------------------------------  | |         | |
    | | |                                                | | |         | |
    | | |                                                | | |         | |
    | | |                                                | | |         | |
    | |  ------------------------------------------------  | |         | |
    |  ----------------------------------------------------   ---------  |
    | x_scroll---------------------------------------------              |
    | |                                                    |             |
    |  ----------------------------------------------------              |
     --------------------------------------------------------------------
    """
    def __init__(self, master=None, scroll_speed:int=2, hscroll:bool=False,
                 vscroll:bool=True, bd:int=0, scrollbar_kwargs={},
                 bg="#f0f0ed", **kwargs):
        assert isinstance(scroll_speed, int), "`scroll_speed` must be an int"
        self.scroll_speed = scroll_speed

        self.master_frame = tk.Frame(master, bd=bd, bg=bg)
        self.master_frame.grid_rowconfigure(0, weight=1)
        self.master_frame.grid_columnconfigure(0, weight=1)
        self.dummy_canvas = tk.Canvas(self.master_frame, highlightthickness=0,
                                      bd=0, bg=bg, **kwargs)
        super().__init__(self.dummy_canvas, bg=bg)

        # Create the 2 scrollbars
        if vscroll:
            self.v_scrollbar = AutoHideScrollbar(self.master_frame,
                                            orient="vertical",
                                            command=self.dummy_canvas.yview,
                                            **scrollbar_kwargs)
            self.v_scrollbar.grid(row=0, column=1, sticky="news")
            self.dummy_canvas.configure(yscrollcommand=self.v_scrollbar.set)
        if hscroll:
            self.h_scrollbar = AutoHideScrollbar(self.master_frame,
                                            orient="horizontal",
                                            command=self.dummy_canvas.xview,
                                            **scrollbar_kwargs)
            self.h_scrollbar.grid(row=1, column=0, sticky="news")
            self.dummy_canvas.configure(xscrollcommand=self.h_scrollbar.set)

        # Bind to the mousewheel scrolling
        self.dummy_canvas.bind_all("<MouseWheel>", self.scrolling_windows,
                                   add=True)
        self.dummy_canvas.bind_all("<Button-4>", self.scrolling_linux, add=True)
        self.dummy_canvas.bind_all("<Button-5>", self.scrolling_linux, add=True)
        self.bind("<Configure>", self.scrollbar_scrolling, add=True)

        # Place `self` inside `dummy_canvas`
        self.dummy_canvas.create_window((0, 0), window=self, anchor="nw")
        # Place `dummy_canvas` inside `master_frame`
        self.dummy_canvas.grid(row=0, column=0, sticky="news")

        self.pack = self.master_frame.pack
        self.grid = self.master_frame.grid
        self.place = self.master_frame.place
        self.pack_forget = self.master_frame.pack_forget
        self.grid_forget = self.master_frame.grid_forget
        self.place_forget = self.master_frame.place_forget

    def scrolling_windows(self, event:tk.Event) -> None:
        assert event.delta != 0, "On Windows, `event.delta` should never be 0"
        y_steps = int(-event.delta/abs(event.delta)*self.scroll_speed)
        self.dummy_canvas.yview_scroll(y_steps, "units")

    def scrolling_linux(self, event:tk.Event) -> None:
        y_steps = self.scroll_speed
        if event.num == 4:
            y_steps *= -1
        self.dummy_canvas.yview_scroll(y_steps, "units")

    def scrollbar_scrolling(self, event:tk.Event) -> None:
        region = list(self.dummy_canvas.bbox("all"))
        region[2] = max(self.dummy_canvas.winfo_width(), region[2])
        region[3] = max(self.dummy_canvas.winfo_height(), region[3])
        self.dummy_canvas.configure(scrollregion=region)

    def resize(self, fit:str=None, height:int=None, width:int=None) -> None:
        """
        Resizes the frame to fit the widgets inside. You must either
        specify (the `fit`) or (the `height` or/and the `width`) parameter.
        Parameters:
            fit:str       `fit` can be either `FIT_WIDTH` or `FIT_HEIGHT`.
                          `FIT_WIDTH` makes sure that the frame's width can
                           fit all of the widgets. `FIT_HEIGHT` is simmilar
            height:int     specifies the height of the frame in pixels
            width:int      specifies the width of the frame in pixels
        To do:
            ALWAYS_FIT_WIDTH
            ALWAYS_FIT_HEIGHT
        """
        if height is not None:
            self.dummy_canvas.config(height=height)
        if width is not None:
            self.dummy_canvas.config(width=width)
        if fit == FIT_WIDTH:
            super().update()
            self.dummy_canvas.config(width=super().winfo_width())
        elif fit == FIT_HEIGHT:
            super().update()
            self.dummy_canvas.config(height=super().winfo_height())
        else:
            raise ValueError("Unknow value for the `fit` parameter.")
    fit = resize


### https://www.geeksforgeeks.org/autohiding-scrollbars-using-python-tkinter/
class AutoHideScrollbar(tk.Scrollbar):
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.tk.call("grid", "remove", self)
        else:
            if self.cget("orient") == 'horizontal':
                self.grid()
            else:
                self.grid()
        tk.Scrollbar.set(self, lo, hi)


class SizeEntry(tk.Frame):
    def __init__(self, parent, var:tk.StringVar, command=None, width:int=5, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)

        self.size = var
        self.entry = IntEntry(self, textvariable=var, command=command, width=width)
        self.entry.pack(side='left')
        self.minus_btn = tk.Button(self, text='\u25BC', width=2, command=lambda: self.increase_size(-2))
        self.minus_btn.pack(side='left')
        self.add_btn = tk.Button(self, text='\u25B2', width=2, command=lambda: self.increase_size(2))
        self.add_btn.pack(side='left')

    def increase_size(self, increment):
        current_size = self.size.get()
        new_size = 0
        if int(current_size) + increment > 0: new_size = int(current_size) + increment
        self.size.set(new_size)
        self.entry.event_generate('<FocusOut>', when='tail')

class IntEntry(ttk.Entry):
    def __init__(self, parent, command, **kwargs):
        self.prevValue = kwargs['textvariable'].get()
        self.command = command
        vcmd = (parent.register(self.validate_int), '%P')
        kwargs['validate'] = 'focusout'
        kwargs['validatecommand'] = vcmd
        ttk.Entry.__init__(self, parent, **kwargs)

        self.bind('<Return>', lambda event: self.event_generate('<FocusOut>', when='tail'))
    
    def validate_int(self, value):
        try:
            value = str(int(value))
            isValid = True
        except:
            isValid = False
        if isValid:
            self.prevValue = value
            if self.command is not None:
                self.command()
        else:
            self.textvariable.set(self.prevValue)
        return isValid

class ColorButton(tk.Frame):
    def __init__(self, parent, variable:tk.StringVar, title:str, cmd=None, **kwargs):
        self.var = variable
        self.cmd = cmd

        tk.Frame.__init__(self, parent, **kwargs)
        self.btn = tk.Button(self, text='', width=2, height=1, background=variable.get(), command=self.choose_color)
        self.btn.pack(side='left')
        self.title = tk.Label(self, text=title)
        self.title.pack(side='right')

    def choose_color(self):
        rgb, color_code = colorchooser.askcolor(title='Choose a color')
        # print(color_code)

        if color_code is not None:
            self.btn['background'] = color_code
            self.var.set(color_code)
            if self.cmd is not None:
                self.cmd()


class Dropdown(ttk.Frame):
    def __init__(self, parent, title, textvariable:tk.StringVar, options, command=None, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.title = tk.Label(self, text=title)
        self.title.pack(side='top')
        self.combobox = ttk.Combobox(self, textvariable=textvariable, state='readonly', values=options, **kwargs)
        if command is not None:
            self.combobox.bind('<<ComboboxSelected>>', command)
        self.combobox.pack(side='bottom')
    
