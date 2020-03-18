# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import os
import sys
import subprocess

if __name__ == '__main__':
	from unisim import route
	from unisim import sim
	Sim_A = sim.Sim("Sim_A", "", "", ["A_1", "A_2", "A_3", "A_4", "A_5"])
	Sim_B = sim.Sim("Sim_B", "", "", ["B_1", "B_2", "B_3", "B_4", "B_5", "B_6"])
	sims = [Sim_A, Sim_B]
	r = ["A_1", "A_3", "B_2", "B_4", "B_5"]
	ret = route.Route().specify(r, sims)
	print("処理前：", r)
	print("処理後：", ret)
