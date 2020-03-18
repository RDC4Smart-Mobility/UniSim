# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import uuid
from random import random
from sumolib import checkBinary
from traci import *

from .sim import Sim
from .route import Route
from .objects import Person
from .objects import Vehicle
from .objects import POI
from .agents import MobileAgent
from .agents import POIAgent
from .agents import Agent
from .repository import MobileAgentRepository
from .repository import POIAgentRepository
from .repository import AgentRepository
from .repository import SimRepository
from .helpers import *
from .api import API
from .db import DB

# SUMO GUI
sumoBinary = checkBinary('sumo-gui')
# SUMO CUI
# sumoBinary = checkBinary('sumo')

class Spawner(object):

    def __init__(self):
        self.spawner = {}

    def add_object(self, depart, obj):
        if not self.spawner.has_key(int(depart)):
            self.spawner[int(depart)] = []
        self.spawner[int(depart)].append(obj)

    def depart_list(self, tick):
        ret = []
        if self.spawner.has_key(int(tick)):
            ret = self.spawner[tick]
        return ret

import json
import subprocess
import xml.dom.minidom

def load_objects(fpath):
    with open(fpath, "r") as file:
        ret = Spawner()
        data = json.load(file)
        for id in data.keys():
            obj = data[id]
            if obj.has_key("depart"):
                obj["id"] = id
                ret.add_object(int(obj["depart"]), obj)
        return ret

def poi_setting(sim_id):
    with open("./poi.json", "r") as file:
        ret = []
        data = json.load(file)
        for poi in data[sim_id].keys():
            entrance = data[sim_id][poi]["entrance"]
            exit = data[sim_id][poi]["exit"]
            capacity = data[sim_id][poi]["capacity"]
            frequency = data[sim_id][poi]["frequency"]
            port = data[sim_id][poi]["provide_info_port"]
            # temp Impl
            ret.append({"poi":POI(poi, entrance, exit, capacity), "freq": frequency, "port": port})
        return ret

def get_edges(file):
    edges = []
    dom = xml.dom.minidom.parse(file)
    for edge in dom.getElementsByTagName("edge"):
        if edge.getAttribute("id")[0] != ":":
            edges.append(edge.getAttribute("id"))
    return edges

def sim_setting():
    with open("./sim.json", "r") as file:
        process_list = []
        sim_list = []
        data = json.load(file)
        for sim_name in data.keys():
            if sim_name == "SUMO":
                sumo_sim_list = data["SUMO"]
                for sim_id in sumo_sim_list.keys():
                    addr = sumo_sim_list[sim_id]["addr"]
                    port = sumo_sim_list[sim_id]["port"]
                    cfg = sumo_sim_list[sim_id]["cfg"]
                    ### cfg => extract net file path => edges
                    net = sumo_sim_list[sim_id]["net"]
                    edges = get_edges(net)
                    sumo_process = subprocess.Popen([sumoBinary, '-c', cfg, '--remote-port', port], stdout=sys.stdout, stderr=sys.stderr)                    
                    API.simulator_init({
                        "type": sim_name,
                        "sim_id": sim_id,
                        "port": port
                        })
                    #traci.init(port=int(port), label=sim_id)
                    sim_list.append(Sim(sim_id, sim_name, port, edges))
                    process_list.append(sumo_process)
            else:
                print("Not SUMO")
        return sim_list, process_list

class UniSim(object):

    def __init__(self):
        self.process_list = None
        self.agent_repository = AgentRepository()
        self.mobile_agent_repository = MobileAgentRepository()
        self.poi_agent_repository = POIAgentRepository()
        self.sim_repository = SimRepository()
        self.spawner = Spawner()
        self._end_step = None
        self.assign_mobile_agent = None #function
        self.master_network = None
        self.db = DB()
        self.run_db = False

    def set_application_link(self, link):
        # link : link type is dict. ex {"app": APP Instance}
        self.app_link = link

    def set_master_network(self, fpath):
        self.master_network = fpath

    def set_db(self, dbpath): # enable to record in db
        self.db.dbpath = dbpath
        self.run_db = True

    # halt all simulation process
    def stop_process(self):
        if self.process_list is not None:
            for process in self.process_list:
                process.wait()

    # initialize simulation step (default step = 0)
    def init_step(self):
        self._step = 1

    # set simulation step ahead
    def advance_step(self, value=1):
        self._step += value

    # set each simulation tick ahead simulation step
    def advance_tick(self):
        for sim_id in self.sim_repository.find_all_ids():
            sim = self.sim_repository.resolve_by_id(sim_id)
            #switch simulation and check (tick < step)
            sim.simulation_step()
        self.next_step()

    # get simulation step
    def get_step(self):
        return self._step

    # set simulation end step
    def end_step(self, end_time):
        self._end_step = end_time

    # check simulation end
    def check_end(self):
        if self._end_step:
            if self.get_step() >= self._end_step:
                return True

    # set poi to sim
    def set_poi(self):
        for sim_id in self.sim_repository.find_all_ids():
            sim = self.sim_repository.resolve_by_id(sim_id)
            for poi_info in poi_setting(sim_id):
                poi = poi_info["poi"]
                sim.poi_repository.store(poi)
                agent_id = uuid.uuid4().hex
                freq = poi_info["freq"]
                ports = poi_info["port"]
                self.poi_agent_repository.store(POIAgent(agent_id, poi, freq, ports))

    # put simulators under Unified Simulator Environment control
    def set_sim(self):
        sim_list, self.process_list = sim_setting()
        for sim in sim_list:
            self.sim_repository.store(sim)

    # load ext info file
    def load(self, fpath):
        self.spawner = load_objects(fpath)

    def assign_mobile_agent(self, obj):
        import uuid
        agent_id = uuid.uuid4().hex
        return Agent(agent_id, obj)

    # main loop
    def simulation_loop(self):
        self.init_step()

        if self.run_db:
            self.db.connect()
            self.db.init_table()

        trans_objects = []

        while True:

            # from spawner
            depart_objects = self.spawner.depart_list(self.get_step())

            for poi_agent in self.poi_agent_repository.find_all():
                if poi_agent.check(self.get_step()):
                    poi_agent.get_information()
                    poi_agent.provide_information(self.get_step())

            for sim_id in self.sim_repository.find_all_ids():
                sim = self.sim_repository.resolve_by_id(sim_id)
                sim.on()

                for obj in depart_objects:
                    factory = ObjectFactory(obj)
                    factory.build()
                    if sim.exist(factory.origin):
                        factory.add_to_simulator(self.sim_repository.find_all())
                        agent, mob = factory.create(self.app_link)
                        if agent is not None:
                            agent.subscribe()
                            self.mobile_agent_repository.store(agent)
                            agent.get_information()
                            # Debug
                            agent.add_information("space", sim_id)

                for trans_object in trans_objects:
                    sim_space, agent = trans_object
                    if sim_id == sim_space:
                        trans_objects.remove(trans_object)
                        API.transfer_object(agent.object_information())
                        agent.subscribe()
                        agent.get_information()
                        agent.update_route_space_info()
                        # Debug
                        agent.add_information("space", sim_space)

                for veh in sim.departed_list():
                    v = Vehicle(veh)
                    sim.vehicle_repository.store(v)

                    agent = self.assign_mobile_agent(v)
                    if agent is not None:
                        if isinstance(agent, MobileAgent):
                            agent.subscribe()
                            agent.get_information()
                            agent.add_information("space", sim_id)
                            agent.add_information("origin", agent.object_information()["edges"][0])
                            agent.add_information("destination", agent.object_information()["edges"][-1])
                            self.mobile_agent_repository.store(agent)

                        if isinstance(agent, Agent):
                            agent.subscribe()
                            agent.get_information()
                            agent.add_information("space", sim_id)
                            self.agent_repository.store(agent)

                for veh in sim.arrived_list():
                    v = sim.vehicle_repository.resolve_by_id(veh)
                    v._discarded = True
                    sim.vehicle_repository.restore(veh)

                # Update Agent - Object Information 
                for agent in filter(lambda e:sim.exist(e.object_information()["road"]), self.agent_repository.find_all()):
                    agent.get_information()
                
                # Update Mobile Agent - Object Information 
                for agent in filter(lambda e:sim.exist(e.object_information()["road"]), self.mobile_agent_repository.find_all()):
                    agent.get_information()

                # For DEBUG All Agent (No Filter)
                #for agent in self.agent_repository.find_all():
                #    print(agent.object_information())

                # For DEBUG All Mobile Agent (No Filter)
                #for agent in self.mobile_agent_repository.find_all():
                #    print(agent.object_information())

                # Process For Agent
                for agent in filter(lambda e:sim.exist(e.object_information()["road"]), self.agent_repository.find_all()):
                    for poi in sim.poi_repository.find_all():
                        if agent.object_information()["road"] == poi.entrance():
                            if poi.enter(self.get_step(), int(random() * 800), agent._object) is not True:
                                agent.object().change_destination(poi.exit())
                        if poi.check_leave(self.get_step()):
                            poi.leave(self.get_step())

                # Process For MobileAgent
                for agent in filter(lambda e:sim.exist(e.object_information()["road"]), self.mobile_agent_repository.find_all()):
                    #agent.debug()
                    #if API.disapper(agent.object_information()):
                    #if not API.exist_next_edge(agent.object_information()):
                    #    API.test_api(agent.object_information())
                    if API.disapper(agent.object_information()):
                        #API.remove_object(agent.object_information())
                        if not agent.object_information()["next_route_space"] == None:
                            index = agent.object_information()["next_route_space"]
                            transfer_space = agent.object_information()["route"][index]
                            sim_space_name = transfer_space.keys()[0]
                            trans_objects.append((sim_space_name, agent))
                        else:
                            agent._discarded = True

                    # agent.depart_sim in sim == True ?
                    #print(agent.object_information())
                    agent.get_information()
                    res = agent.use_app()    # temp impl
                    if not res == None:
                        obj_type = agent.object_information()["type"]
                        obj_id = agent.object_information()["id"]
                        current_position = agent.object_information()["road"]
                        destination = agent.object_information()["destination"]
                        if len(self.sim_repository.find_all()) > 1:
                            route = router(self.master_network, obj_id, current_position, destination, obj_type)
                            agent.add_information("route", Route().specify(route, self.sim_repository.find_all()))
                            agent.add_information("destination", agent.object_information()["route"][0].values()[0][-1])
                            agent.update_route_space_info()
                        API.change_destination(agent.object_information())
                        agent.get_information()

                    if agent._relation:
                        agent._relation.share_information(agent)
                    # agent._information.road in poi.entrance?
                    for poi in sim.poi_repository.find_all():
                        if agent.object_information()["road"] == poi.entrance():
                            if poi.enter(self.get_step(), int(random() * 800), agent._object) is not True:
                                agent.object().change_destination(poi.exit())
                        if poi.check_leave(self.get_step()):
                            poi.leave(self.get_step())

                sim.simulation_step()

            for agent in self.mobile_agent_repository.find_all(): # add (lng, lat) information
                geo = simulation.convertGeo(agent.object_information()["position"][0], agent.object_information()["position"][1], False)
                agent.add_information("lng", geo[0])
                agent.add_information("lat", geo[1])

            # Record All Object Information
            if self.run_db:
               self.db.store(self.get_step(), self.mobile_agent_repository.find_all() + self.agent_repository.find_all())

            self.advance_step()
            if self.check_end():
                for sim_id in self.sim_repository.find_all_ids():
                    sim = self.sim_repository.resolve_by_id(sim_id)
                    sim.close()
                return



class ObjectFactory(object):

    def __init__(self, obj):
        self.obj = obj
        self.params = {}
        self.origin = ""
        self.route_space = None

    def build(self):
        for key in self.obj.keys():
            if key == "type":
                self.params["type"] = self.obj["type"]
                continue
            if key == "id":
                self.params["id"] = self.obj["id"]
                continue
            if key == "route":
                self.params["route"] = self.obj["route"].split(" ")
                self.origin = self.params["route"][0]
                continue
            self.params[key] = self.obj[key]


    def add_to_simulator(self, sims):
        #self.build()
        if self.params["type"] == "pedestrian":
            id = self.params["id"]
            route = self.params["route"]
            self.params["route_space"] = None
            self.params["route_space"] = Route().specify(route, sims)
            API.add_object(self.params)

#            if(len(self.params["route_space"]) == 1):
#                #api_add_pedestrian(id, route, 0, 1)
#                API.add_object(self.params)
#            else:
#                print("This route includes multi sim space edge.")
#                print(self.params["route_space"][0].values()[0])
#                #api_add_pedestrian(id, self.route_space[0].values()[0], 0, 1)
#                API.add_object(self.params)


    def get_origin(self):
        return self.origin

    def get_route(self):
        return self.params["route_space"]

    def create(self, app_link):
        agent = None
        mob = None
        if self.params["type"] == "pedestrian":
            mob = Person(self.params["id"])
        if self.params["type"] == "vehicle":
            mob = Vehicle(self.params["id"])
        if self.params.has_key("agent"):
            agent_id = uuid.uuid4().hex
            client = []
            if self.params.has_key("app"):
                app_list = self.params["app"].split(" ")
                client = [app_link[e] for e in app_list]
            agent = MobileAgent(agent_id, mob, client)
            agent.add_information("route", self.params["route_space"])
            if (len(self.params["route_space"]) == 1):
                agent.add_information("next_route_space", None)
            else:
                index = 1
                agent.add_information("next_route_space", index)
        return (agent, mob)

