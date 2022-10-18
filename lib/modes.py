
DEFAULT_SLEEP_TIME = 1
RAINBOW_MODULO = 5

class HSVT:
    def __init__(this, hue, sat, volume, temp=None):
        this.hue = hue
        this.sat = sat
        this.volume = volume
        this.temp = temp
        this.id = f'{this.hue or 0}-{this.sat or 0}-{this.volume or 0}-{this.temp or 0}'

    def __str__(this):
        this.id

def christmas():
    yield HSVT(0,100,100)
    yield HSVT(120,100,100)
    yield HSVT(None,None,100,4000)

def merica():
    yield HSVT(0,100,100)
    yield HSVT(None,None,100,4000)
    yield HSVT(240,100,100)

def v_day():
    yield HSVT(0,100,100)
    yield HSVT(320,100,100)

def st_pat():
    yield HSVT(120,61,50)
    yield HSVT(120,100,50)
    yield HSVT(120,100,20)

def glow():
    yield HSVT(249,61,22)

def rainbow():
    for i in range(360):
        if i % RAINBOW_MODULO == 0:
            yield HSVT(i,100,100)

def halloween():
    for h in range(0,40):
        for v in range(0,100):
            yield HSVT(h,100,i)

class Mode:
    def __init__(this, sync, random, transition_time, sleep_time, colors):
        this.sync = sync
        this.random = random
        this.transition_time = transition_time
        this.sleep_time = sleep_time if sleep_time is not None else DEFAULT_SLEEP_TIME
        this.colors = list(colors)

    def __str__(this):
        return f'Sync: {this.sync}\nRandom: {this.random}\nTransition time: {this.transition_time}\nSleep time: {this.sleep_time}\nColors: {this.colors}'

modes = {}
#                         sync,  random trans sleep colors
modes['CHRISTMAS'] = Mode(False, True,  1000, 4,    christmas())
modes['MERICA'] =    Mode(True,  False, None, 2.5,  merica())
modes['VDAY'] =      Mode(True,  False, None, None, v_day())
modes['STPAT'] =     Mode(True,  False, None, 2.5,  st_pat())
modes['GLOW'] =      Mode(True,  False, None, None, glow())
modes['RAINBOW'] =   Mode(True,  False, 50,   0.05, rainbow())
modes['DISCO'] =     Mode(False, True,  10,   0.01, rainbow())
modes['HALLOWEEN'] = Mode(False, True,  150,  0.15, halloween())

def list():
    return '\n\t'.join(modes.keys())
