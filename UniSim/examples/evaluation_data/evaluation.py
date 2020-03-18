# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import os
import sys
import subprocess

from unisim import UniSim
from unisim import MobileAgent
from unisim import Agent

def assign_mobile_agent(veh):
    from sample_client import Client
    import uuid
    agent_id = uuid.uuid4().hex
    # No ITS Service - Test Case -
    #return Agent(agent_id, veh)
    # All Object has ITS Service - Test Case -
    return MobileAgent(agent_id, veh, [Client("", 4001)])

if __name__ == "__main__":

    unified_simulator = UniSim()

    unified_simulator.set_sim()
    unified_simulator.set_master_network("./data3/osm.net.xml")
    unified_simulator.end_step(3600)

    unified_simulator.assign_mobile_agent = assign_mobile_agent

    unified_simulator.simulation_loop()

    unified_simulator.stop_process()