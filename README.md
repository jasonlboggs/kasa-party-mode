# kasa-party-mode

This module utilizes the `python-kasa` libary to create several party modes for TP-Link Kasa Color Smart Bulbs (specifically the KL130).  It assumes all Kasa Smart Bulbs are on the same subnet as the machine that this code will run on.


## Installation
### Install python-kasa (https://github.com/python-kasa/python-kasa)
```
sudo pip3 install python-kasa
```

### Clone and make executable
```
git clone https://github.com/jasonlboggs/kasa-party-mode.git
cd kasa-party-mode
chmod 755 party.py
```

## Usage
### Args: ModeName, Bulb IP list
```
./party.py Merica, 100,101,102,103
```

### Modes
Execute party.py without any params or see `lib/modes.py` for available modes
