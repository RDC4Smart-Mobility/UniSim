# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import os
import sys
from random import random

from unisim import BaseServer

PARKING_LIST = ['p2en', 'p3en']
data = {}

class ParkingServer(BaseServer):
    
    def deal_msg(self, sock, msg, readfds):
        if len(msg) == 0:
            sock.close()
            readfds.remove(sock)

        elif msg == 'get_parking':
            if float(data["Parking2"]) <= float(data["Parking3"]):
                parking = PARKING_LIST[0]
            else:
                parking = PARKING_LIST[1]
            sock.send(parking)

        else:
            res = msg.split(" ")
            if res[0] == "info":
                name = res[1].split(":")[1]
                porp = res[4].split(":")[1]
                data[name] = porp
                if res[5].split(":")[1] == "3990":
                    exit()
            print(msg)

if __name__ == '__main__':
    ParkingServer("", 4002).run()