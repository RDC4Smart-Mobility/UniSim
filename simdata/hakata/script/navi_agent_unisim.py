# -*- coding: utf-8 -*-
from __future__ import absolute_import

import traci
from unisim import MobileAgent
from unisim import Routine

from navi_interfaces_unisim import NaviReceiverInterface, LocationSenderInterface

class NaviUserMentalUniSim(Routine):
    def __init__(self):
        self._done = False
    
    def accept(self):
        if not self._done:
            self._done = True
            return True
        else:
            return False

class NaviAgentUniSim(MobileAgent):
    def __init__(self, id, obj):
        MobileAgent.__init__(self, id, obj, [NaviReceiverInterface(), LocationSenderInterface()])
        self._routine = NaviUserMentalUniSim()
        self._newViaList = None
    
    def use_app(self):
        if not self.discarded():
            if self._apps:
                # 反則技
                self._information["isStoppedParking"] = traci.vehicle.isStoppedParking(self._information["id"])

                for app in self._apps:
                    if app.event_handler(self.object_information()):
                        app.run()
                        if isinstance(app, NaviReceiverInterface):
                            self._newViaList = app._res

            if self._newViaList:
                if self._routine.accept():
                    # 反則技
                    vehID = self._information['id']
                    traci.vehicle.setVia(vehID, self._newViaList)
                    target_edge = traci.vehicle.getRoute(vehID)[-1]
                    self.change_object_destination(target_edge)
