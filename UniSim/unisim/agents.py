# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

from .api import API
from .wrappers import BaseClient

class Entity(object):
    pass

class Routine(object):
    def __init__(self):
        self.acceptable_range = 100
        
    def accept(self):
        from random import random
        return random()*100 <= self.acceptable_range

class MobileAgent(Entity):

    def __init__(self, id, obj, apps):
        self._id = id
        self._routine = Routine()
        self._object = obj
        self._information = {}
        self._discarded = False
        self._apps = apps
        self._relation = None
        self._used = False
        self._information["type"] = obj.type()
        self._information["id"] = obj.id()


    def id(self):
        return self._id

    def routine(self):
        return self._routine

    def object(self):
        return self._object

    def object_information(self):
        return self._information

    def add_information(self, key, value):
        self._information[key] = value

    def change_object_destination(self, destination):
        params["destination"] = destination
        self.check_discarded()
        if not self.discarded():
            API.change_destination(self._information)

    def subscribe(self):
        if not self.discarded():
            API.subscribe(self._information)

    def get_information(self):
        self.check_discarded()
        if not self.discarded():
            #self._information = self._object.update_information()
            self._information.update(API.get_information(self._information))

    def update_route_space_info(self):
        next_space_index = 1
        if not self._information.has_key("next_route_space"):
            self.add_information("next_route_space", None)
        if self._information["next_route_space"]:
            next_space_index = self._information["next_route_space"] + 1
        if (len(self._information["route"]) == next_space_index):
                self.add_information("next_route_space", None)
        elif not self._information["next_route_space"]:
                self.add_information("next_route_space", next_space_index)


    def discarded(self):
        return self._discarded

    def check_discarded(self):
        if self._object.discarded():
            self._discarded = True

    def use_app(self):
        if not self.discarded():
            if self._apps:
                for app in self._apps:
                    if app.event_handler(self.object_information()) and not self._used:
                        app.run()
                        self._used = True
                        ## 操作
                        if self.routine().accept():
                            # Routing
                            self.add_information("destination", app._res)
                            return app._res
                            #Route().specify(route, sims)
                            #API.change_destination(self.object_information())
                            #self._object.change_destination(app._res)
        return None

class POIAgent(Entity):

    def __init__(self, id, poi, freq, ports):
        self._id = id
        self._poi = poi
        self._information = None
        self._frequency = freq
        self._ports = ports
        self._provider = [BaseClient("", port) for port in self._ports]

    def id(self):
        return self.id

    def poi(self):
        return self._poi

    def poi_information(self):
        return self._information

    def get_information(self):
        self._information = self.poi().information()

    def provide_information(self, step):
        for e in self._provider:
            e.send_information("info %s step:%d" % (self.poi_information(), step))
        #return "info %s" % self.poi_information()

    def check(self, step):
        if step % self._frequency == 0:
            return True

class Agent(Entity):

    def __init__(self, id, obj):
        self._id = id
        self._object = obj
        self._information = {}
        self._discarded = False
        self._information["type"] = obj.type()
        self._information["id"] = obj.id()

    def id(self):
        return self._id

    def routine(self):
        return self._routine

    def object(self):
        return self._object

    def object_information(self):
        return self._information

    def add_information(self, key, value):
        self._information[key] = value

    def subscribe(self):
        if not self.discarded():
            API.subscribe(self._information)

    def get_information(self):
        self.check_discarded()
        if not self.discarded():
            #self._information = self._object.update_information()
            self._information.update(API.get_information(self._information))

    def discarded(self):
        return self._discarded

    def check_discarded(self):
        if self._object.discarded():
            self._discarded = True
