#! /bin/python2

import subprocess

####################################################
#
#   methods to enable and disable monitor
#       mode for the wifi card (if possible)
#
####################################################

def disableInterface(interface):
    airmon = subprocess.Popen(['airmon-ng','stop',interface],stdout=subprocess.PIPE)
    grep_mode = subprocess.Popen(['grep','mode'],stdin=airmon.stdout,stdout=subprocess.PIPE)
    grep_monitor = subprocess.Popen(['grep','monitor'],stdin=grep_mode.stdout,stdout=subprocess.PIPE)
    grep_enable = subprocess.Popen(['grep','enable'],stdin=grep_monitor.stdout,stdout=subprocess.PIPE)

    end_of_pipe = grep_enable.stdout
    out = ""

    for line in end_of_pipe:
        out += line
    
    if out == "":
        return True
    return False

def enableInterface(interface):
    airmon = subprocess.Popen(['airmon-ng','start',interface],stdout=subprocess.PIPE)
    grep_mode = subprocess.Popen(['grep','mode'],stdin=airmon.stdout,stdout=subprocess.PIPE)
    grep_monitor = subprocess.Popen(['grep','monitor'],stdin=grep_mode.stdout,stdout=subprocess.PIPE)
    grep_enable = subprocess.Popen(['grep','enable'],stdin=grep_monitor.stdout,stdout=subprocess.PIPE)

    end_of_pipe = grep_enable.stdout
    out = ""

    for line in end_of_pipe:
        out += line
    
    if out == "":
        return False
    return True
