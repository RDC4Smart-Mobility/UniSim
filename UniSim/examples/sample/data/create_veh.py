# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

from random import random

RESPAWN = ["res1", "res2", "res3"]
DESPAWN = ["des1", "des2", "des3"]

PARKING = ["p1en", "p2en", "p3en"]

class Veh(object):
    def __init__(self, orig, dest, app):
        self._origin = orig
        self._destination = dest
        self._app = app
        
    def info(self):
        ret = "%s %s %s" %(self._origin, self._dest, self._app)
        return ret
    
def app_checker():
    v = int(random() * 100)
    if v <= 30:
        return "App1"
    elif v <= 40:
        return "App2"
    else:
        return "None"

def gen_res():
    v = int(random() * 100)
    if v <= 40:
        return RESPAWN[0]
    elif v <= 80:
        return RESPAWN[1]
    else:
        return RESPAWN[2]
        
def gen_des():
    v = int(random() * 100)
    if v <= 40:
        return DESPAWN[0]
    elif v <= 80:
        return DESPAWN[1]
    else:
        return DESPAWN[2]
        
if __name__ == "__main__":
    vehs = []
    for i in range(120):
        o = gen_res()
        d = gen_des()
        app = app_checker()
        veh = Veh(o, d, app)
        vehs.append(veh)
    for v in vehs:
        print(v._origin)