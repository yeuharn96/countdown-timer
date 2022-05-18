import datetime as dt
target = None
target_date = dt.datetime.now()

def set_time(hh=None, mm=None):
    if hh is not None and mm is not None:
        target['time']['hh'].set(hh)
        target['time']['mm'].set(mm)

    hour = int(target['time']['hh'].get())
    minute = int(target['time']['mm'].get())

    now = dt.datetime.now()
    if hour < now.hour:
        now += dt.timedelta(days=1)
    global target_date
    target_date = now.replace(hour=hour, minute=minute, second=0)
    # print('target_time',target_date)

def set_duration(hh=None, mm=None):
    if hh is not None and mm is not None:
        target['duration']['hh'].set(hh)
        target['duration']['mm'].set(mm)
    hour = int(target['duration']['hh'].get())
    minute = int(target['duration']['mm'].get())
    global target_date
    target_date =  dt.datetime.now() + dt.timedelta(hours=hour, minutes=minute)
    # print('target_duration',target_date, hour, minute)

def add_duration(hh=0, mm=0, ss=0):
    global target_date
    target_date += dt.timedelta(hours=int(hh), minutes=int(mm), seconds=int(ss))

def get_timedelta():
    td = target_date - dt.datetime.now()
    over_time = td.days < 0
    if over_time: td = dt.datetime.now() - target_date
    # print(target_date, dt.datetime.now(), td)
    total_min, second = divmod(td.seconds, 60)
    hour, minute = divmod(total_min, 60)
    return hour, minute, second, over_time

def get_now():
    return  dt.datetime.now().strftime('%I:%M:%S %p')
