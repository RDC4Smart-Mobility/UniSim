# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import os
import sys
import subprocess
from random import random
import uuid

# from unisim import UniSim
from unisim import MobileAgent

from unisim import UniSim
# from database import DB2

from datetime import datetime

import threading
# from RESTserver import app, Flask_DB
# from unisim import app, Flask_DB

from unisim.RESTserver import dbstart

# Other
def assign_mobile_agent(veh):
    agent_id = uuid.uuid4().hex
    return MobileAgent(agent_id, veh, [])

if __name__ == "__main__":

    dbpath = datetime.now().strftime("%Y-%m-%d-%H:%M:%S") + ".db"

    unified_simulator = UniSim()
    unified_simulator.set_sim()
    unified_simulator.set_master_network("../hakata-tenjin.notjam.net.xml")
    # unified_simulator.end_step(4000)
    unified_simulator.assign_mobile_agent = assign_mobile_agent
    unified_simulator.set_db(dbpath) # enable db
    # unified_simulator.simulation_loop()
    thread_1 = threading.Thread(target=unified_simulator.simulation_loop)
    
    # Flask_DB.dbpath = dbpath
    # Flask_DB.connect()
    thread_2 = threading.Thread(target=dbstart, args=(dbpath, 5000))

    thread_1.start()
    thread_2.start()
