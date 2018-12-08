import os
import netifaces
import time
import subprocess

import probe

greeting = """
*********************************************************
*                                                       *
*   Setting up the network interface to ~ H A C K ~     *
*                                                       *
*********************************************************
    This script will search for network interfaces
and attempt to configure one to monitor mode.  If 
no interface can be monitor mode enabled, deauth attacks
are impossible.

Note:
Requires the netifaces python module and sudo privileges.
"""


def getInterfaces():
    interfaces = netifaces.interfaces()
    if len(interfaces) == 0:
        print("No interfaces found. Exiting...")
        exit()

    print str(len(interfaces)) + " interfaces found. Enter the number the interface you'd like to use: "

    for i in range(len(interfaces)):
        print " (" + str(i + 1) + ") " + interfaces[i]
    
    choice = raw_input(">>> ")
    if int(choice) not in range(1, len(interfaces) + 1):
        print('invalid choice, exiting')
        exit()

    return { "interfaces" : interfaces, "selection" : interfaces[int(choice) - 1] } 

def testForMonitorMode():
    print "\n"
    print "*********************************************************"
    print "Running iwconfig...\n"

    interfaces = netifaces.interfaces()

    for interface in interfaces:
        iw_config = subprocess.check_output(['iwconfig',str(interface)])
        print(iw_config)
        iw_config = iw_config.split()

        for item in iw_config:
            if item.startswith("Mode"):
                splitItem = item.split(":")
                if splitItem[1] == "Monotor":
                    return True

    return False


'''
interfaces = netifaces.interfaces()

print 'These interfaces found: '
print interfaces

os.system('airmon-ng start ' + str(interfaces[2]))

time.sleep(2)
interfaces = netifaces.interfaces()

print 'These interfaces found: '
print interfaces

'''

def main():
    print greeting
    
    print "Attempting to enable monitor mode..."
    
    time.sleep(2)

    res = getInterfaces()
    interface = res["selection"]
    
    print "Attempting to enable interface " + interface + "..."
    enabled = probe.enableInterface(interface)
    if not enabled:
        print "Unable to enable monitor mode for iterface " + interface + "."
        print "Please try again or just give up, you loser."
        exit()

    print "Successfully enabled monitor mode for interface " + interface + "."
    time.sleep(2)
    pre_interfaces = set(res["interfaces"]) - set(interface)
    post_interfaces = set(netifaces.interfaces())

    print "Auto detecting and configuring iface for deauth attacks..."
    time.sleep(2)

    hack_interface = post_interfaces - pre_interfaces
    hacker_face = list(hack_interface)[0]

    print "Detected new interface " + hacker_face
    print "Writing configuration to .config.txt..."
    time.sleep(2)

    with open('.config.txt','w') as f:
        f.write("NORMAL_INTERFACE:" + interface)
        f.write("\n")
        f.write("MONITOR_INTERFACE:" + hacker_face)

    print "Successfully wrote configuration to .config.txt"
    print "Disabling monitor mode on interface " + hacker_face + " for now."

    time.sleep(2)
    print "Attempting to disable interface " + interface + "..."
    disabled = probe.disableInterface(hacker_face)
    if disabled:
        print "Successfully disabled interface " + interface + " from monitor mode."
        print "Testing successful."

    exit()

if __name__ == "__main__":
    main()
