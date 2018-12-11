import scapy.all

import os,sys,signal
import time
import threading
import probe 
import copy

SCAN_ACCURACY = 200

class Scanner(object):
    networks = {}

    def __init__(self):
        # map of the networks { <Mac address> : <bytes string of wifi name> (if available)  }
        self.networks = {}              

        # the interface name for the wifi in normal mode
        self.normal_iface = None

        # the interface name for the wifi in monitor mode
        self.monitor_iface = None

        # is the scannerscanning?
        self.active = False
        self.loadConfig()

    # loads the network configuration information to allow the scanner to 
    #   automatically turn the wifi card to MONITOR mode and back to normal
    #   mode
    def loadConfig(self):
        lines = []
        with open('.config.txt','r') as f:
            for line in f:
                lines.append(line)
        for line in lines:
            if line.split(":")[0] == "NORMAL_INTERFACE":
                self.normal_iface = line.split(":")[1].strip()
            elif line.split(":")[0] == "MONITOR_INTERFACE":
                self.monitor_iface = line.split(":")[1].strip()

        if self.normal_iface == None and self.monitor_iface == None:
            print "Could not load configuration. Exiting..."
            exit()

    #####################################################################
    # enter and exit
    #       allow the class to be 'withable'
    #       allows for loose RAII when used with a with statement
    #       (see deauth.py for an example)
    #####################################################################

    def __enter__(self):
        status = probe.enableInterface(self.normal_iface)
        if not status:
            print "Unable to turn on monitor mode for " + self.normal_iface
            exit()

        # create scanner 
        pid = os.fork()
        if pid == 0:
            self.channelSurf()
        else:
            self.child = pid

        return self

    def __exit__(self,exc_type,exc_value,traceback):
        if self.active:
            self.stopScanning()
        probe.disableInterface(self.monitor_iface) 
        os.kill(self.child,signal.SIGTERM)
        

    # internal method to change the channel the wifi scanner is listening on
    #   you shouldn't need to use this
    def channelSurf(self):
        channel = 1
        while True:
            os.system("iw dev %s set channel %d" % (self.monitor_iface,channel))
            channel = 1 if channel + 1 == 14 else channel + 1
            time.sleep(1)

    # scans the network for wifi access points
    # SCAN_ACCURACY - a loose way to change the length of the scan
    #       it is defined at the top of the file, make the value smaller 
    #       to scan for less time but potentially miss more networks
    def scanNetworks(self):
        channel = 1
        for i in range(SCAN_ACCURACY):
            self.pkt_cout = 0
            scapy.all.sniff(iface=self.monitor_iface, prn=self.handler,stop_filter=lambda count : self.pkt_cout < 50000)
                        
    # handler - called whenever the sniffer finds a packet
    # filters through the packets, extracts the MAC address and 
    # stores it into the network if not there map
    def handler(self,pkt):
        self.pkt_cout += 1
        if (pkt.haslayer(scapy.all.Dot11)):
            if pkt.type == 0 and pkt.subtype == 8:
                ssid = pkt[scapy.all.Dot11Elt].info
                bssid = pkt[scapy.all.Dot11].addr3

                if bssid.strip() not in self.networks.keys():
                    if len(ssid.strip()) != 0 and ssid.strip() != '\x00':
                        self.networks[bssid.strip()] = ssid.strip()
    # gets a copy of the networks currently contained in the scanner object
    def getNetworks(self):
        return copy.deepcopy(self.networks)
