# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import sys
import socket
from contextlib import closing

from unisim import BaseCallApi
from unisim import API

class Client(BaseCallApi):

    def event_handler(self, info):
        if info["road"] == "84515125#3":
                self._cmd = "get_parking"
                return True

    def get_parking(self, params={}):
        params["url"] = self.url + "points/"
        params["method"] = "GET"
        return self.call_api(params)
        
    def operate_application(self, cmd):
        if cmd == "get_parking":
            self.get_parking({"id":3})
        
    def interpreter(self):
        item = self.response[0]
        lat = item['lat']
        lng = item['lng']
        self._res, _, _ = API.change_destination_from_geo({
            "type": "SUMO",
            "lat": lat,
            "lng": lng
            })


if __name__ == '__main__':
    pass
