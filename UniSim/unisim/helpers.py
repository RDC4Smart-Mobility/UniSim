#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import os
import sys
import subprocess
import xml.dom.minidom

def which(bin):
	try:
		cmd = ["which", bin]
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
		res = p.stdout.readlines()
		if len(res) == 0:
			raise Exception("%s not found", bin)
		return os.path.realpath(res[0].strip())
	except:
		if os.path.isfile(bin):
			return os.path.realpath(bin)
		else:
			raise Exception("%s not found", bin)

def router(net, veh_id, current_position, destination, type="vehicle"):
	duarouter = which("duarouter")
	if type == "vehicle":
		with open("tmp.xml", mode = "w") as f:
			f.write("<trips>\n")
			f.write('   <trip id="%s" depart="0.00" from="%s" to="%s" />\n' % (veh_id, current_position, destination))
			f.write("</trips>\n")
	if type == "pedestrian":
		with open("tmp.xml", mode = "w") as f:
			f.write('<person id="0" depart="0.00">\n')
			f.write('   <walk from="%s" to="%s"/>\n' % (current_position, destination))
			f.write("</person>\n")

	os.system('duarouter -n ' + net + ' -t tmp.xml -o tmp.rou.xml')
	dom = xml.dom.minidom.parse("tmp.rou.xml")
	e = dom.getElementsByTagName("route").item(0)
	if not e:
		e = dom.getElementsByTagName("walk").item(0)
	list = e.getAttribute("edges").split(" ")
	return list

if __name__ == '__main__':
	router(sys.argv[1], 0, sys.argv[2], sys.argv[3], "pedestrian")
	
