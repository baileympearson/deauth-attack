#!/usr/bin/env python2

import time
from scanner import Scanner 
from attacker import Attacker

# Taco bell wifi hard coded for the example - remove this
WIFI = 'c8:d7:19:5d:df:9b'

scanner = Scanner()
with scanner as s:
    print 'scanning networks'
    s.scanNetworks()

    # create the attacker obj
    #   gotta pass in the monitor_iface from the scanner
    #   to make it work
    attacker = Attacker(s.monitor_iface)
    attacker.startAttack()

    i = 1
    for item in s.networks.keys():
        print " " + str(i) + ") " + str(item)
        i += 1
    network = raw_input("select network: ")
    networks = [s.networks.keys()[int(network) - 1]]

    networks = s.networks.keys()

    attacker.updateQueue(networks)

    time.sleep(45)
    exit()

    networks = [s.networks.keys()[int(network) - 1], WIFI]
    attacker.updateQueue(networks)

    time.sleep(15)

    networks = [WIFI]
    attacker.updateQueue(networks)

    inp = raw_input('press q to quit')
    attacker.stopAttack()
