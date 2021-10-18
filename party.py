#!/usr/bin/env python3

import sys
import time
import socket
import random
import asyncio
from lib import kasabulb, modes
from kasa import SmartBulb

def list_modes():
    print(f'Available party modes:\n\t{modes.list()}')

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def set_ips(ips):
    _ips = ips
    ip_parts = get_ip_address().split('.')
    subnet = '.'.join(ip_parts[:3])
    for i,ip in enumerate(_ips):
        _ips[i] = f'{subnet}.{ip}'
    return _ips

def check_args():
    if len(sys.argv) < 3:
        print('Invalid arguments')
        print('Usage: ./party.py ModeName 100,101,102,103')
        list_modes()
        exit(-1)

async def init_bulb(IP):
    bulb = None
    try:
        bulb = SmartBulb(IP)
        await bulb.update()
        print(f'Found Bulb: {bulb.alias}')
    except Exception as ex:
        print(f'Error initializing {IP}: {ex}')
        bulb = None
    return bulb

async def get_bulbs():
    bulbs = []
    input_ips = sys.argv[2].split(',')
    ips = set_ips(input_ips)

    for ip in ips:
        smartbulb = await init_bulb(ip)
        if smartbulb is not None:
            bulbs.append(kasabulb.KasaBulb(smartbulb))
    return bulbs

async def stop():
    print('WARNING: Quitting Party mode!')
    bulbs = await get_bulbs()
    for bulb in bulbs:
        await bulb.turnoff()
    sys.exit(0)

async def start():
    check_args()
    desired_mode = sys.argv[1]
    try:
        active_mode = modes.modes[desired_mode.upper()]
    except KeyError:
        print(f'Mode "{desired_mode}" not found')
        list_modes()
        exit(-1)

    DEBUG = False if len(sys.argv) < 4 else True
    bulbs = await get_bulbs()
    i = 0

    while True:
        if bulbs is None or len(bulbs) == 0:
            bulbs = await get_bulbs()

        if len(bulbs) == 0:
            print('No valid bulbs found')
            exit(-1)

        i += 1
        i = i % len(active_mode.colors)
        if active_mode.random:
            hsvt = random.choice(active_mode.colors)
        else:
            hsvt = active_mode.colors[i]

        if DEBUG: print ('------------------------------------------------------------------------------')
        tasks = []
        for bulb in bulbs:
            print_val = ''
            if not active_mode.sync:
                current_hsvt = modes.HSVT(bulb.bulb.hsv[0], bulb.bulb.hsv[1], bulb.bulb.hsv[2], bulb.bulb.color_temp)
                available_colors = [color for color in active_mode.colors if color.id != current_hsvt.id]
                hsvt = random.choice(available_colors)
                print_val = f'{current_hsvt.id} --> '
            tasks.append(asyncio.create_task(bulb.set(hsvt, active_mode.transition_time, not active_mode.sync)))
            print_val += hsvt.id
            if DEBUG: print (print_val)
        await asyncio.wait(tasks)

        time.sleep(active_mode.sleep_time)

if __name__ == '__main__':
    try:
       asyncio.run(start())
    except KeyboardInterrupt:
       asyncio.run(stop())
