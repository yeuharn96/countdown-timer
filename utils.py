import os
from pathlib import Path
import json
import tkinter as tk


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
DEFAULT_SETTING = {
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

class AppSetting:
  @staticmethod
  def load():
    def merge_settings(s1, s2):
      for key in s1:
        if key in s2:
          if isinstance(s1[key], dict) and isinstance(s2[key], dict):
            merge_settings(s1[key], s2[key])
          elif s1[key] != s2[key]: 
            s1[key] = s2[key]
      return s1
    
    app_setting = {}
    if os.path.exists(SETTING_FILE_PATH):
      f = open(SETTING_FILE_PATH, 'r')
      try: savedSetting = json.load(f)
      except: savedSetting = {}
      f.close()
      app_setting = merge_settings(DEFAULT_SETTING, savedSetting)
    else:
      app_setting = DEFAULT_SETTING

    iterate_json(app_setting, lambda data, key, value: tk.StringVar(value=value))
    return app_setting

  @staticmethod
  def save(setting):
    dirname = os.path.dirname(SETTING_FILE_PATH)
    Path(dirname).mkdir(parents=True, exist_ok=True)      
    f = open(SETTING_FILE_PATH, 'w')
    iterate_json(setting, lambda data, key, value: value.get())
    f.write(json.dumps(setting, indent=2))
    f.close()


  