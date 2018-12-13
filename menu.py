# -*- coding: utf-8 -*-
import time
from consolemenu import *
from consolemenu.items import *
import threading
import sys

import attacker
import scanner


class menuHandler:
    sub_menu_size = 10

    def __init__(self):
        self.menu_list = []
        self.cur_menu_index = 0

    def load_menus(self, dic):
        data = list(dic)
        self.menu_list = []
        cur_list = []
        for i in range(len(data)):
            cur_list.append(data[i])
            if len(cur_list) == menuHandler.sub_menu_size:
                self.menu_list.append(cur_list)
                cur_list = []

        if len(cur_list) != 0:
            self.menu_list.append(cur_list)

        self.cur_menu_index = 0

    def generate_current_menu(self):
        menu = ConsoleMenu('Choose a Network to Disable >:)', 'Page: ' + str(self.cur_menu_index + 1), show_exit_option=False)
        
        # load in actual menu contents
        for val in self.menu_list[self.cur_menu_index]:
            menu.append_item(FunctionItem(val, toggle_network, args=[val]))

        # all menus except first should have back option
        if self.cur_menu_index != 0:
            menu.append_item(FunctionItem('Previous Page', previous_page))
        
        # all menus except last should have go forward option
        if self.cur_menu_index != len(self.menu_list) - 1:
            menu.append_item(FunctionItem('Next Page', next_page))

        # all menus should be able to refresh or exit
        menu.append_item(FunctionItem('Refresh', refresh))
        menu.append_item(FunctionItem('Exit', selfdestruct))

        return menu

    def next(self):
        self.cur_menu_index += 1

    def prev(self):
        self.cur_menu_index -= 1

def refresh():
    time.sleep(1)
    scan.scanNetworks()
    mh.load_menus(scan.getNetworks())
    active_menu = mh.generate_current_menu()
    active_menu.show()
    sys.exit(0)

# exit the program
def selfdestruct():
    attack.stopAttack()
    sys.exit(0)    

# change menu to the next page
def next_page():
    time.sleep(1)
    mh.next()
    active_menu = mh.generate_current_menu()
    active_menu.show()
    sys.exit(0)

# change menu to the previous page
def previous_page():
    time.sleep(1)
    mh.prev()
    active_menu = mh.generate_current_menu()
    active_menu.show()
    sys.exit(0)

# toggle whether the given network @ address is accessable or not
def toggle_network(address):
    if address in targets:
        targets.remove(address)
    else:
        targets.append(address)

    attack.updateQueue(targets)
    

# networks currently being disabled
targets = []

# to scan for networks
scanr = scanner.Scanner()

with scanr as scan: 
    scan.scanNetworks()

    # to attack networks
    iface = scan.monitor_iface
    attack = attacker.Attacker(iface)
    attack.startAttack()

    # 'graphical' interface setup
    mh = menuHandler()
    mh.load_menus(scan.getNetworks())
    menu = mh.generate_current_menu()
    menu.show()
