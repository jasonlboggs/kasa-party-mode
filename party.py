#!/usr/bin/env python3

#  Install python-kasa
#  $ sudo pip3 install python-kasa

#Usage:
#./party.py Merica '100,101,102,103'

import sys
import time
import socket
import signal
import random
import asyncio
import multiprocessing
from lib import kasabulb, modes
from kasa import SmartBulb
from multiprocessing.pool import ThreadPool as Pool

def list_modes():
    print(f'Available party modes:\n\t{modes.list()}')

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def set_ips():
    ip_parts = get_ip_address().split('.')
    subnet = '.'.join(ip_parts[:3])
    for i,ip in enumerate(IPs):
        IPs[i] = f'{subnet}.{ip}'

def init_bulb(IP):
    bulb = None
    try:
        bulb = SmartBulb(IP)
        asyncio.run(bulb.update())
        print(f'Found Bulb: {bulb.alias}')
    except Exception as ex:
        print(f'Error initializing {IP}: {ex}')
        bulb = None
    return bulb

def get_bulbs():
    bulbs = []
    for IP in IPs:
        smartbulb = init_bulb(IP)
        if smartbulb is not None:
            bulbs.append(kasabulb.KasaBulb(smartbulb))
    return bulbs

def stop(sig, frame):
    print('WARNING: Quitting Party mode!')
    bulbs = get_bulbs()
    for kasabulb in bulbs:
        kasabulb.turnoff()

    sys.exit(0)

if len(sys.argv) != 3:
    print('Invalid arguments')
    print('Usage: ./party.py ModeName 100,101,102,103')
    list_modes()
    exit(-1)

DESIRED_MODE = sys.argv[1]
IPs = sys.argv[2].split(',')

signal.signal(signal.SIGINT, stop)

set_ips()

try:
    active_mode = modes.modes[DESIRED_MODE]
except KeyError:
    print(f'Mode "{DESIRED_MODE}" not found')
    list_modes()
    exit(-1)

i = 0
bulbs = None

print(f'Computed IPs: {IPs}')

while True:
    if bulbs is None or len(bulbs) == 0:
        bulbs = get_bulbs()

    if len(bulbs) == 0:
        print('No valid bulbs found')
        exit(-1)

    i += 1
    i = i % len(active_mode.colors)
    hsvt = random.choice(active_mode.colors) if active_mode.random else active_mode.colors[i]

    processes = []
    for bulb in bulbs:
        if not active_mode.sync:
            hsvt = random.choice(active_mode.colors)
        p = multiprocessing.Process(target=bulb.set, args=(hsvt, active_mode.transition_time,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    time.sleep(active_mode.sleep_time)
