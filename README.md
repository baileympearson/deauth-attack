# deauth-attack

## Usage
Must be run as sudo.
```
	sudo python2 deauth.py
```

## Dependencies 
Uses python2.

### Python dependencies:
	- scapy
	- threading

### Other Dependencies
You must have a wifi card with monitor mode enabled.  For simplicity, I have 
added a back script that uses airmon-ng to enable the wireless card in my computer.
However, to use the program you will need to figure out how to enable 
monitor mode for your own device.

## TODO
	- automate enabling of monitor mode
	- add user interface and network selection


