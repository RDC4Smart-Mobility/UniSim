# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import os
import sys
import subprocess
from random import random
import uuid

from unisim import UniSim
from unisim import MobileAgent


def assign_mobile_agent(veh):
    from sample2_client import Client
    value = random() * 100
    agent_id = uuid.uuid4().hex
    if veh.id() == "0.2":
        return MobileAgent(agent_id, veh, [Client()])
    else:
        return None

if __name__ == "__main__":

    unified_simulator = UniSim()
    unified_simulator.set_sim()
    unified_simulator.set_master_network("./data/ito.net.xml")
    
    unified_simulator.end_step(4000)
    unified_simulator.assign_mobile_agent = assign_mobile_agent
    unified_simulator.simulation_loop()

    unified_simulator.stop_process()