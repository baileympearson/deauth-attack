# -*- coding: utf-8 -*-
import time
from consolemenu import *
from consolemenu.items import *
import threading
import sys


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
            menu.append_item(FunctionItem(val, disable_network))

        # all menus except first should have back option
        if self.cur_menu_index != 0:
            menu.append_item(FunctionItem('Previous Page', previous_page))
        
        # all menus except last should have go forward option
        if self.cur_menu_index != len(self.menu_list) - 1:
            menu.append_item(FunctionItem('Next Page', next_page))

        # all menus should be able to refresh or exit
        menu.append_item(FunctionItem('Refresh', change_menu))
        menu.append_item(FunctionItem('Exit', selfdestruct))

        return menu

    def next(self):
        self.cur_menu_index += 1

    def prev(self):
        self.cur_menu_index -= 1

def change_menu():
    time.sleep(1)
    menu2 = menu_from_dict('Choose a Network to Disable', '', {'network1': '55:55:55:55:55', 'network3': '1:1:1:1:1', 'network4': '4:3:2:1:0'})
    menu2.show()
    sys.exit(0)

def selfdestruct():
    sys.exit(0)    

def next_page():
    time.sleep(1)
    mh.next()
    active_menu = mh.generate_current_menu()
    active_menu.show()
    sys.exit(0)

def previous_page():
    time.sleep(1)
    mh.prev()
    active_menu = mh.generate_current_menu()
    active_menu.show()
    sys.exit(0)

def disable_network():
    pass

sample = {str(i) for i in range(30)}
mh = menuHandler()
mh.load_menus(sample)
menu = mh.generate_current_menu()
menu.show()
