import tkinter as tk
from tkinter import simpledialog, messagebox
from custom_widgets import ScrollableListbox, AskStringDialog
from utils import AppSetting, find
import copy

app_profiles = None
app_profiles_current = None
def _find_profile(key, find_value=None, default=None):
    if find_value is None: find_value = app_profiles_current['profile'][key]
    return find(app_profiles, lambda p: p['profile'][key] == find_value, default)

def get_current():
    return app_profiles_current
def set_current(profile_id=None):
    prev = _find_profile('id')
    curr = _find_profile('id', profile_id)
    if prev is not None:
        AppSetting.merge_from_stringvar(prev, app_profiles_current) # save changes made on previous profile
    if curr is not None:
        for p in app_profiles: p['profile']['selected'] = '0'
        curr['profile']['selected'] = '1'
        AppSetting.merge_to_stringvar(app_profiles_current, curr) # load selected profile values

def _update_changes():
    curr = _find_profile('id')
    if curr is not None: AppSetting.merge_from_stringvar(curr, app_profiles_current) # update changes
    
def get_all():
    _update_changes()
    return app_profiles


def set_all(profiles):
    '''this function only run once on app startup'''
    global app_profiles
    app_profiles = profiles
    # default select first if not selected
    selected = _find_profile('selected', '1', app_profiles[0])
    global app_profiles_current
    app_profiles_current = copy.deepcopy(selected)

def get_all_names():
    return [p['profile']['name'] for p in get_all() + get_all()]

def remove_from_list(profile_name):
    item = _find_profile('name', profile_name)
    if item is not None:
        app_profiles.remove(item)
        # if profile to remove is current selected, default to first profile
        if item['profile']['id'] == app_profiles_current['profile']['id']:
            set_current(app_profiles[0]['profile']['id'])


def add_to_list(profile_name):
    new_profile = AppSetting.default()
    new_profile['profile']['name'] = profile_name
    app_profiles.append(new_profile)

def edit_name(old_name, new_name):
    to_edit = _find_profile('name', old_name)
    if to_edit is not None:
        to_edit['profile']['name'] = new_name
        # if profile to edit is current selected
        if to_edit['profile']['id'] == app_profiles_current['profile']['id']:
            app_profiles_current['profile']['name'] = new_name


class ProfilePane(tk.Frame):
    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)


        self.profiles = tk.StringVar(value=get_all_names())
        self.selected_profile = None

        self.win = self.init_win()
        self.win.withdraw()

        self.init_widgets()

    def init_widgets(self):
        tk.Label(self, text='Profile: ', anchor='w').pack(fill='both')
        tk.Button(self, text='Switch Profile', command=self.win.deiconify).pack(fill='both')
    
    def init_win(self):
        # if self.win is not None:
        #     self.win.lift()
        #     self.win.focus_force()
        #     return

        win = tk.Toplevel()
        win.title('Manage Profiles')
        w, h = 320, 320
        x, y = (win.winfo_screenwidth() - w) // 2, (win.winfo_screenheight() - h) // 2
        win.geometry(f'{w}x{h}+{x}+{y}')
        win.protocol("WM_DELETE_WINDOW", lambda: self.win.withdraw())


        confirm_frame = tk.Frame(win)
        confirm_frame.pack(side='bottom')
        tk.Button(confirm_frame, text='Select Profile', width=10).pack(side='left', padx=5, pady=10)
        tk.Button(confirm_frame, text='Cancel', width=10, command=lambda: self.win.withdraw()).pack(side='right', padx=5, pady=10)

        sl = ScrollableListbox(win, 'Switch Profile', self.profiles, lambda idx, selected: self.on_select_profile(selected))
        sl.pack(side='left', fill='both', expand=True, padx=(10,0))
        sl.listbox['activestyle'] = 'none'
        sl.listbox.selection_set(0)
        # sl.listbox.selection_clear(0,'end')

        cmd_frame = tk.Frame(win)
        cmd_frame.pack(side='right')
        tk.Button(cmd_frame, text='\u2795 Add', width=10,
            command=lambda: self.on_add_edit('add')).pack(padx=10, pady=5)
        tk.Button(cmd_frame, text='\u270E Edit', width=10
            command=lambda: self.on_add_edit('edit')).pack(padx=10, pady=5)
        tk.Button(cmd_frame, text='\u274C Delete', width=10,
            command=lambda: self.on_delete(self.selected_profile)).pack(padx=10, pady=5)

        return win

    def on_select_profile(self, selected):
        self.selected_profile = selected

    def on_add_edit(self, cmd, initialvalue=''):
        title=''
        if cmd == 'add': title = 'New Profile'
        elif cmd == 'edit': title = 'Edit Profile'
        profile_name = AskStringDialog.show(title=title, prompt='Profile name: ', initialvalue=initialvalue)
        if profile_name is None: return

        # profile_name = simpledialog.askstring(title='Add Profile', prompt='Profile name: ', initialvalue=initialvalue)
        if profile_name in self.profiles.get(): messagebox.showerror(title='Duplicate profile', message='Profile name already exists, please choose another name.')
        if cmd == 'add': print('append to list')
        elif cmd == 'edit': print('edit profile name')
    
    def on_delete(self, profile_name):
        message = f'Confirm delete profile: {profile_name} ?'
        confirm_delete = messagebox.askyesno(title='Delete Profile', message=message)
        if confirm_delete: print('delete from list')
