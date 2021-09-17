import asyncio
from kasa import SmartBulb

class KasaBulb:
    def __init__(this, bulb):
        this.bulb = bulb

    def set(this, hsvt, trans):
        try:
            if hsvt.temp is not None:
                asyncio.run(this.bulb.set_brightness(hsvt.volume, transition=trans))
                asyncio.run(this.bulb.set_color_temp(hsvt.temp, transition=trans))
            else:
                asyncio.run(this.bulb.set_hsv(hsvt.hue, hsvt.sat, hsvt.volume, transition=trans))

            asyncio.run(this.bulb.update())
        except Exception as ex:
            print(f'Error with set(): {ex}')

    def turnoff(this):
        try:
            asyncio.run(this.bulb.turn_off())
        except Exception as ex:
            print(f'Error with turnoff(): {ex}')
