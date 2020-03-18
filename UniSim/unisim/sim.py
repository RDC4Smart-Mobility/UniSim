# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

from .repository import VehicleRepository
from .repository import POIRepository
from .api import API

class Entity(object):
    pass

class Sim(Entity):

    def __init__(self, id, type, port, edges):
        self._id = id
        self._type = type
        self._port = port
        self._edges = edges
        self.vehicle_repository = VehicleRepository()
        self.poi_repository = POIRepository()
        
    def id(self):
        return self._id

    def type(self):
        return self._type
        
    def departed_list(self):
        return API.departed({
            "type": self.type(),
            "id": self.id()
            })
        
    def arrived_list(self):
        return API.arrived({
            "type": self.type(),
            "id": self.id()
            })
        
    def simulation_step(self):
        API.simulation_step({
            "type": self.type(),
            "id": self.id()
            })

    def on(self):
        API.simulator_switch({
            "type": self.type(),
            "id": self.id()
            })

    def close(self):
        API.simulator_close({
            "type": self.type(),
            "id": self.id()
            })    

    def exist(self, edge):
        return edge in self._edges