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
    agent_id = uuid.uuid4().hex
    return MobileAgent(agent_id, veh, [])

if __name__ == "__main__":

    unified_simulator = UniSim()
    unified_simulator.set_sim()
    unified_simulator.set_master_network("./data/ito.net.xml")
 
    unified_simulator.end_step(900)
    unified_simulator.assign_mobile_agent = assign_mobile_agent
    unified_simulator.simulation_loop()

    unified_simulator.stop_process()
