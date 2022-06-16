import tkinter as tk
from tkinter.font import Font
from monitors import monitor_areas
from custom_widgets import IntEntry
from profile import ProfilePane
import timer


class OutputPane(tk.Frame):
  def __init__(self, parent, setting, **kwargs):
    tk.Frame.__init__(self, parent, **kwargs)

    self.win_output = None
    # self.output_title = None
    self.output_text = None
    self.setting = setting

    self.init_widgets()

  def init_widgets(self):
    btn_show = tk.Button(self, text='Show', fg='red', bg='#DDD', font=Font(size=16, weight='bold'),
      command=self.show_output
    ).grid(row=0, column=0, ipady=5, pady=(0, 5), sticky='new')

    tk.Button(self, text='Hide', fg='gray', bg='#DDD', font=Font(size=16, weight='bold'),
      command=self.hide_output
    ).grid(row=1, column=0, ipady=5, sticky='new')

    config_frame = tk.Frame(self)
    config_frame.grid(row=2, column=0, pady=(15,0), sticky='ew')
    tk.Radiobutton(config_frame, text='Config 1', variable=self.setting['config'],
                    value=1
                   ).grid(row=0, column=0)
    tk.Radiobutton(config_frame, text='Config 2', variable=self.setting['config'],
                    value=2
                   ).grid(row=0, column=1)
    
    pos_frame = tk.Frame(self, highlightbackground='black', highlightthickness=1)
    pos_frame.grid(row=3, column=0, pady=(15,5), ipady=5, sticky='we')
    def label_entry(pf, label, var):
      frame = tk.Frame(pf)
      tk.Label(frame, text=label).grid(row=0, column=0, sticky='we')
      IntEntry(frame, textvariable=var, width=5, command=self.apply_output_config).grid(row=1, column=0)
      return frame
    tk.Label(pos_frame, text='Adjustment', font=Font(size=12, weight='bold'), anchor='w').pack(fill='both')
    _pf = tk.Frame(pos_frame)
    _pf.pack()
    label_entry(_pf, label='top', var=self.setting['adj_pos']['top']).grid(row=1, column=1)
    label_entry(_pf, label='left', var=self.setting['adj_pos']['left']).grid(row=2, column=0)
    label_entry(_pf, label='right', var=self.setting['adj_pos']['right']).grid(row=2, column=2)
    label_entry(_pf, label='bottom', var=self.setting['adj_pos']['bottom']).grid(row=3, column=1)

    ProfilePane(self).grid(row=4, column=0, sticky='we')


  def init_win_output(self):
    self.win_output = tk.Toplevel()
    self.win_output.overrideredirect(1)
    self.win_output.bind('<Escape>', lambda event: self.hide_output())
    
    center_frame = tk.Frame(self.win_output)
    # self.output_title = tk.Label(center_frame, text='')
    # self.output_title.pack(side='top', fill='x')
    self.output_text = tk.Label(center_frame, text='')
    self.output_text.pack(side='bottom', fill='x')
    center_frame.place(relx=0.5, rely=0.5, anchor='center')


  def apply_output_config(self):
    if self.win_output is None: return

    mon = monitor_areas()
    # print(mon)
    if len(mon) == 1:
      x, y, w, h = mon[0]
    elif int(self.setting['config'].get()) == 1:
      x, y, w, h = mon[0][2], mon[0][1], mon[0][2], mon[0][3]
    else:
      x, y, w, h = mon[1][0], mon[1][1], mon[1][2]-mon[1][0], mon[1][3]-mon[1][1]
    
    # print('calc',x,y,w,h)
    def calc_adj_pos(pos, geo):
      val = self.setting['adj_pos'][pos].get()
      try: val = int(val)
      except: val = 0
      geo += val
      return 0 if geo < 0 else geo
    y = calc_adj_pos('top', y)
    x = calc_adj_pos('left', x)
    w = calc_adj_pos('right', w)
    h = calc_adj_pos('bottom', h)
    # print('calc2',x,y,w,h)

    self.win_output.geometry("{}x{}+{}+{}".format(w,h,x,y))
    self.win_output.config(bg=self.setting['bg'].get())

    # self.output_title.config(
    #   text=self.setting['title'].get(),
    #   bg=self.setting['bg'].get(),
    #   fg=self.setting['fg'].get(), 
    #   font=(self.setting['font'].get(), 
    #   int(self.setting['size'].get()))
    # )

    self.output_text.config(
      bg=self.setting['bg'].get(),
      fg=self.setting['fg'].get(), 
      font=(self.setting['font'].get(), 
      int(self.setting['size'].get()))
    )


  def show_output(self):
    def refresh_timer():
      txt = ''
      title_txt = self.setting['title'].get()
      if len(title_txt) > 0:
        txt += title_txt + '\n'
      if self.setting['show-clock'].get() == '1':
        txt += timer.get_now() + '\n'
      if self.setting['show-timer'].get() == '1':
        hour, minute, second, over_time = timer.get_timedelta()
        txt += '+' if over_time else ''
        txt += f'{hour:02}h {minute:02}m {second:02}s'
      self.output_text.config(text=txt)
      self.output_text.after(1000, refresh_timer)
    if self.win_output is None: self.init_win_output()
    self.apply_output_config()
    refresh_timer()
    self.win_output.lift()

  def hide_output(self):
    if self.win_output is not None:
      self.win_output.destroy()
      self.win_output = None
      





