from kasa import SmartBulb

class KasaBulb:
    def __init__(this, bulb):
        this.bulb = bulb

    async def set(this, hsvt, trans, update_after):
        try:
            if hsvt.temp is not None:
                await this.bulb.set_brightness(hsvt.volume, transition=trans)
                await this.bulb.set_color_temp(hsvt.temp, transition=trans)
            else:
                await this.bulb.set_hsv(hsvt.hue, hsvt.sat, hsvt.volume, transition=trans)

            if update_after:
                await this.bulb.update()
        except Exception as ex:
            print(f'Error with set(): {ex}')

    async def turnoff(this):
        try:
            await this.bulb.turn_off()
        except Exception as ex:
            print(f'Error with turnoff(): {ex}')
