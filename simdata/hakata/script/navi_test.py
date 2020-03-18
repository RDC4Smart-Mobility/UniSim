# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import os
import sys
import subprocess

from unisim import UniSim
from unisim import MobileAgent

from dummy_db import DummyDB
from navi_agent_unisim import NaviAgentUniSim

def assign_mobile_agent(veh):
    import uuid

#    if veh.id() == 'hakata_guchi.0':
    if veh.id() == 'veh_with_navi.0':
        agent_id = uuid.uuid4().hex
        return NaviAgentUniSim(agent_id, veh)

if __name__ == '__main__':
    unified_simulator = UniSim()
    unified_simulator.db = DummyDB()

    unified_simulator.set_sim()
#     unified_simulator.set_master_network("./data/hakata-tenjin.net.xml")
    unified_simulator.end_step(25500)

    unified_simulator.assign_mobile_agent = assign_mobile_agent

    unified_simulator.simulation_loop()

    unified_simulator.stop_process()


