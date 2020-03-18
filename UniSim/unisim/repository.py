# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals
from abc import ABCMeta, abstractmethod

from .objects import Vehicle
from .objects import POI
from .agents import MobileAgent
from .agents import POIAgent
from .agents import Agent

class Repository(object):
    
    __metaclass__ = ABCMeta

    @abstractmethod
    def store(self, obj):
        raise NotImplementedError

    @abstractmethod
    def resolve_by_id(self, id):
        raise NotImplementedError

    @abstractmethod
    def find_all(self):
        raise NotImplementedError

    @abstractmethod
    def find_all_ids(self):
        raise NotImplementedError

class SimRepository(Repository):
    
    def __init__(self):
        self._sims = {}
    
    def store(self, sim):
        #if not isinstance(sim, Sim):
        #    raise TypeError
        self._sims[sim.id()] = sim
        
    def resolve_by_id(self, id):
        return self._sims[id]

    def find_all(self):
        return self._sims.values()

    def find_all_ids(self):
        return self._sims.keys()

class VehicleRepository(Repository):

    def __init__(self):
        self._vehicles = {}

    def store(self, vehicle):
        if not isinstance(vehicle, Vehicle):
            raise TypeError
        self._vehicles[vehicle.id()] = vehicle
        
    def restore(self, id):
        del self._vehicles[id]

    def resolve_by_id(self, id):
        return self._vehicles[id]

    def find_all(self):
        return self._vehicles.values()

    def find_all_ids(self):
        return self._vehicles.keys()

class POIRepository(Repository):

    def __init__(self):
        self._pois = {}

    def store(self, poi):
        if not isinstance(poi, POI):
            raise TypeError
        self._pois[poi.name()] = poi

    def resolve_by_id(self, id):
        return self._pois[id]

    def find_all(self):
        return self._pois.values()

    def find_all_ids(self):
        return self._pois.keys()

class MobileAgentRepository(Repository):

    def __init__(self):
        self._agents = {}

    def store(self, agent):
        if not isinstance(agent, MobileAgent):
            raise TypeError
        self._agents[agent.id()] = agent

    def resolve_by_id(self, id):
        return self._agents[id]

    def find_all(self):
        return filter(lambda e: not e.discarded(), self._agents.values())

    def find_all_ids(self):
        return filter(lambda e: not e.discarded(), self._agents.keys())

class POIAgentRepository(Repository):

    def __init__(self):
        self._agents = {}

    def store(self, agent):
        if not isinstance(agent, POIAgent):
            raise TypeError
        self._agents[agent.id()] = agent

    def resolve_by_id(self, id):
        return self._agents[id]

    def find_all(self):
        return self._agents.values()

    def find_all_ids(self):
        return self._agents.keys()

class AgentRepository(Repository):

    def __init__(self):
        self._agents = {}

    def store(self, agent):
        if not isinstance(agent, Agent):
            raise TypeError
        self._agents[agent.id()] = agent

    def resolve_by_id(self, id):
        return self._agents[id]

    def find_all(self):
        return filter(lambda e: not e.discarded(), self._agents.values())

    def find_all_ids(self):
        return filter(lambda e: not e.discarded(), self._agents.keys())

if __name__ == "__main__":
    pass
