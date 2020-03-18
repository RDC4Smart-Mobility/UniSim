# -*- coding:utf-8 -*-
from __future__ import print_function

import urllib2
import json

import traci

from unisim import BaseCallApi

# NAVI_SERVER = 'http://localhost:3000/'
NAVI_SERVER = 'http://json-server:80/'
"""
WEBApiサーバの指定
"""


class NaviReceiverInterface(BaseCallApi):
    """
    WebApiから情報取得
    """
    def __init__(self):
        self.url = NAVI_SERVER
        self._used = False
    
    def event_handler(self, info):
        if not self._used and info['isStoppedParking']:
            print('Vehicle is Parking, and Driver operates NaviApp now.')
            self._cmd = 'get_vialist'
            return True
            
        else:
            return False

    def get_vialist(self, params={}):
        params['url'] = self.url + 'vialist'
        params['method'] = 'GET'
        return self.call_api(params)

    def operate_application(self, cmd):
        if cmd == 'get_vialist':
            self.get_vialist()

    def interpreter(self):
        json_dict = self.response

        vialist = []
        for via in json_dict:
            if isinstance(via['lng'], unicode):
                lng = float(via['lng'].decode('unicode-escape'))
            else:
                lng = via['lng']

            if isinstance(via['lat'], unicode):
                lat = float(via['lat'].decode('unicode-escape'))
            else:
                lat = via['lat']
            
            via_road, _, _, = traci.simulation.convertRoad(lng, lat, True, 'passenger')

            if ':' not in via_road:
                vialist.append(via_road)

        print("vialist: ", vialist)
        self._res = vialist
        self._used = True


class LocationSenderInterface():
    """
    自車位置を標準出力に出力
    """
    def _init__(self):
        self._currentLocInfo = None

    def event_handler(self, info):
        if info['isStoppedParking']:
            return False
        else:
            x, y = info['position']
            angle = info['angle']
            lng, lat = traci.simulation.convertGeo(x, y, False)

            self._currentLocInfo = json.dumps({'longitude': lng, 'latitude': lat, 'angle': angle})
            return True

    def run(self):
        print("Current LocInfo: ", self._currentLocInfo)
        return