# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

#TODO
##from infrastructure.sumoapi import (api_get_position, api_get_destination, api_get_speed, api_set_color, api_get_road, api_change_destination, api_get_origin)
##from .api import (api_get_position, api_get_destination, api_get_speed, api_set_color, api_get_road, api_change_destination, api_get_origin)
#TODO END

class Entity(object):
    pass

class Person(Entity):

    def __init__(self, id):
        self._id = id
        self._type = "pedestrian"
        self._discarded = False
        self._color = False
        self.information = {}

    def id(self):
        return self._id

    def type(self):
        return self._type

#    def change_destination(self, destination):
#        ## check destination edge in this sim
#        api_change_destination(self.id(), destination)

    def discarded(self):
        return self._discarded
        
#    def change_color(self, color):
#         api_set_color(self.id(), color)

class VehicleInformation(object):

    def __init__(self):
        self.origin = None
        self.destination = None
        self.route = []

    def params(self):
        return self.__dict__

class Vehicle(Entity):

    def __init__(self, id):
        self._id = id
        self._type = "vehicle"
        self._discarded = False
        self._color = False
        self._information = VehicleInformation()

    def id(self):
        return self._id

    def type(self):
        return self._type

#    def update_information(self):
#        self._information.origin = api_get_origin(self.id())
#        self._information.position = api_get_position(self.id())
#        self._information.road = api_get_road(self.id())
#        self._information.destination = api_get_destination(self.id())
#        self._information.speed = api_get_speed(self.id())
#        return self._information
#
#
#    def change_destination(self, destination):
#        ## check destination edge in this sim
#        api_change_destination(self.id(), destination)

    def discarded(self):
        return self._discarded
        
#    def change_color(self, color):
#         api_set_color(self.id(), color)

class POI(object):

    def __init__(self, name, entrance, exit, capacity):
        self._name = name
        self._entrance = entrance
        self._exit = exit
        self._capacity = capacity
        self._number = 0
        ## temp code
        self.repos = []

    def name(self):
        return self._name

    def entrance(self):
        return self._entrance

    def exit(self):
        return self._exit

    def enter(self, step, duration, object, number = 1):
        if self.repos:
            vehs = map(lambda x: x.object, self.repos)
            if not object in vehs:
                if number <= self.allowed_number():
                    self._number += number
                    self.repos.append(StayInfo(step, duration, object))
                else:
                    return False
        else:
            self._number += number
            self.repos.append(StayInfo(step, duration, object))
        return True

    def leave(self, step):
        vehs = filter(lambda x: x.depart_step == step, self.repos)
        self._number -= len(vehs)
        for v in vehs:
            self.repos.remove(v)

    def check_leave(self, step):
        if self.repos:
            v = map(lambda x: x.depart_step, self.repos)
            if v.count(step):
                return True
        else:
            return False


    def allowed_number(self):
        return self._capacity - self._number

    def information(self):
        proportion = float(self._number)/self._capacity * 100
        return "name:%s max_capacity:%d number:%d proportion:%.2f"%( self._name, self._capacity, self._number, proportion)

class StayInfo(object):
    def __init__(self, step, duration, object):
        self.arrive_step = step
        self.depart_step = step + duration
        self.object = object


