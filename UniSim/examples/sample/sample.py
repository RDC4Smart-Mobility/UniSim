# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import os
import sys
import subprocess

from unisim import UniSim
from unisim import MobileAgent
from unisim import Agent

def assign_mobile_agent(veh):
    from random import random
    from sample_client import Client
    import uuid
    value = random() * 100
    agent_id = uuid.uuid4().hex
    if 0 <= value < 40:
        return MobileAgent(agent_id, veh, [Client("", 4001)])
    elif 40 <= value < 70:
        return MobileAgent(agent_id, veh, [Client("", 4002)])
    else:
        return Agent(agent_id, veh)

if __name__ == "__main__":

    unified_simulator = UniSim()

    unified_simulator.set_sim()
    unified_simulator.set_poi()
    unified_simulator.set_master_network("./data/sim.net.xml")
    unified_simulator.end_step(4000)

    unified_simulator.assign_mobile_agent = assign_mobile_agent

    unified_simulator.simulation_loop()

    unified_simulator.stop_process()