from pydispatch import dispatcher

__time__ = 0

def execute(time_range = [], aircraft = []):

    dispatcher.send(
        'sim-init',
        sender = 'Simulator',
        time = 0,
        data = 'Initializing simulation'
    )

    global __time__

    for t in time_range:
        set_time(t)
        for plane in aircraft:
            plane.fly()

def get_time():
    global __time__
    return __time__

def set_time(t):
    global __time__
    __time__ = t