import os
from pathlib import Path
import json
import tkinter as tk
import uuid

def iterate_json(data, func):
  for key,value in data.items():
    if isinstance(value, dict):
      iterate_json(value, func)
    elif isinstance(value, list):
      for val in value:
        if isinstance(val, str):
          pass
        elif isinstance(val, list):
          pass
        else:
          iterate_json(val)
    else:
      data[key] = func(data, key, value)

SETTING_FILE_PATH = os.getenv('LOCALAPPDATA') + r'\pptx-py\countdown-timer.setting'

class AppSetting:
  @staticmethod
  def default():
    return {
      'profile': { 'id': uuid.uuid4().hex, 'name': 'default', 'selected': '0' },

      'bg':'black',
      'fg': 'white',
      'size': '14',
      'title': '',
      'font': 'Arial',
      'show-timer': '1',
      'show-clock': '0',

      'config': '1',
      'adj_pos':{
        'left': '0',
        'right': '0',
        'top': '0',
        'bottom': '0'
      }
    }

  @staticmethod
  def load(handle_change):
    app_settings = [AppSetting.default()]
    if os.path.exists(SETTING_FILE_PATH):
      f = open(SETTING_FILE_PATH, 'r')
      try:
        saved_setting = json.loads(f.read())
        if type(saved_setting) == dict: saved_setting = [saved_setting]
        app_settings = saved_setting
      except Exception as e:
        print('error load', str(e))
      f.close()

    # def wrap_var(data, key, value):
    #   sv = tk.StringVar(value=value)
    #   sv.trace_id = sv.trace('w', lambda *args: handle_change())
    #   return sv
    for idx, setting in enumerate(app_settings):
      # ensure there is no missing setting fields
      app_settings[idx] = AppSetting.merge(AppSetting.default(), setting)
      # iterate_json(app_settings[idx], wrap_var)
    return app_settings

  @staticmethod
  def merge(s1, s2, assign_func=None):
    for key in s1:
      if key in s2:
        if isinstance(s1[key], dict) and isinstance(s2[key], dict):
          AppSetting.merge(s1[key], s2[key], assign_func)
        elif assign_func is not None:
          assign_func(s1, s2, key)
        elif s1[key] != s2[key]:
          s1[key] = s2[key]
    return s1

  @staticmethod
  def merge_to_stringvar(s1, s2):
    def assign(s1, s2, key):
      if isinstance(s1[key], tk.StringVar): s1[key].set(s2[key])
    return AppSetting.merge(s1, s2, assign)

  @staticmethod
  def merge_from_stringvar(s1, s2):
    def assign(s1, s2, key):
      if isinstance(s2[key], tk.StringVar): s1[key] = s2[key].get()
    return AppSetting.merge(s1, s2, assign)

  @staticmethod
  def save(settings):
    dirname = os.path.dirname(SETTING_FILE_PATH)
    Path(dirname).mkdir(parents=True, exist_ok=True)      
    f = open(SETTING_FILE_PATH, 'w')
    f.write(json.dumps(settings, indent=2))
    f.close()


def find(lst, expr, default=None):
  return next((item for item in lst if expr(item)), default)
  