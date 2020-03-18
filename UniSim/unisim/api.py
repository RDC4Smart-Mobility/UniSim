# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import traci

#
# Get Common Variable from TraCI
# http://sumo.dlr.de/wiki/TraCI/Person_Value_Retrieval
# http://sumo.dlr.de/wiki/TraCI/Vehicle_Value_Retrieva
#
COMMON_VARIABLE = {
    0x40 : "speed",
    0x42 : "position",
    0x43 : "angle",
    0x50 : "road",
    0x56 : "lane_position"
}

# 
# Get Vehicle Variable from TraCI
# http://sumo.dlr.de/wiki/TraCI/Vehicle_Value_Retrieval
#
VEHICLE_VARIABLE = {
    0x51 : "lane",
    0x54 : "edges",
    0x84 : "distance"
}

# Variable for SUMO
person_variables = COMMON_VARIABLE
vehicle_variables = dict(COMMON_VARIABLE.items() + VEHICLE_VARIABLE.items())

class SimulatorApi(object):
    
    def __init__(self):
        pass

    def subscribe(self, params):
        if params["type"] == "pedestrian":
            try:
                perID = params["id"]
                variable_ids = person_variables.keys()
                traci.person.subscribe(perID, varIDs=variable_ids)
            except Exception as e:
                raise e
            finally:
                pass
        if params["type"] == "vehicle":
            try:
                vehID = params["id"]
                variable_ids = vehicle_variables.keys()
                traci.vehicle.subscribe(vehID, varIDs=variable_ids)
            except Exception as e:
                raise e
            finally:
                pass

    def add_object(self, params):
        if params["type"] == "pedestrian":
            try:
                perID = params["id"]
                if(len(params["route_space"]) == 1):
                    route = params["route"]
                else:
                    print("This route includes multi sim space edge.")
                    print(params["route"])
                    print("- - - - - - - - - - - - - - - - - - - - -")
                    route = params["route_space"][0].values()[0]
                position = params["position"] if params.has_key("position") else 0
                speed = params["speed"] if params.has_key("speed") else 1.0
                traci.person.add(perID, route[0], position)
                traci.person.appendWalkingStage(perID, route, 0.0)
                traci.person.setSpeed(perID, speed)
            except Exception as e:
                raise e
            finally:
                print("Call API: Add Object (Pedestrian)")

        if params["type"] == "vehicle":
            # NOT IMPL YET
            try:
                vehID = params["id"]
                destination = params["destnation"]
                traci.vehicle.changeTarget(vehID, destination)
            except Exception as e:
                raise e
            finally:
                print("Call API: Add Object (Vehicle)")

    def change_destination(self, params):
        
        if params["type"] == "pedestrian":
            try:
                perID = params["id"]
                route = params["route"]
                position = params["position"]
                speed = params["speed"] if params.has_key("speed") else 1.0
                traci.person.removeStages(perID)                
                #traci.person.add(perID, route[0].values()[0][0], int(position))
                traci.person.appendWalkingStage(perID, route[0].values()[0], 0, speed=1.0)
                traci.person.appendWaitingStage(perID, 1)
            except Exception as e:
                raise e
            finally:
                pass
                print("Call API: Change destination")

        if params["type"] == "vehicle":
            # NOT IMPL YET
            try:
                vehID = params["id"]
                destination = params["destination"]
                traci.vehicle.changeTarget(vehID, destination)
            except Exception as e:
                raise e
            finally:
                pass
                #print("Call API: Change Destination")

    def get_information(self, params):
        parameters = {}
        res = {}
        parameters["type"] = params["type"]
        if params["type"] == "pedestrian":
            try:
                perID = params["id"]
                res = traci.person.getSubscriptionResults(perID)
                if res:
                    for e in res:
                        parameters[person_variables.get(e)] = res.get(e)
            except Exception as e:
                raise e
            finally:
                pass
                #print("Call API: Get Object Information")
        if params["type"] == "vehicle":
            try:
                vehID = params["id"]
                #route = traci.vehicle.getRoute(vehID)
                #parameters["origin"] = route[0]
                #parameters["destination"] = route[-1]
                res = traci.vehicle.getSubscriptionResults(vehID)
                if res:
                    for e in res:
                        # Pass to Overwrite Road Information If Road is Junction
                        if vehicle_variables.get(e) == "road":
                            if not res.get(e) in res.get(0x54):
                                continue
                        parameters[vehicle_variables.get(e)] = res.get(e)
            except Exception as e:
                raise e
            finally:
                pass
                #print("Call API: Get Object Information")
        return parameters

    def remove_object(self, params):
        if params["type"] == "pedestrian":
            try:
                perID = params["id"]
                stage_index = 0
                traci.person.removeStage(perID, stage_index)
            except Exception as e:
                raise e
            finally:
                pass
        if params["type"] == "vehicle":
            # NOT IMPL YET
            try:
                pass
            except Exception as e:
                raise e
            finally:
                pass
        return False

    def transfer_object(self, params):
        if params["type"] == "pedestrian":
            try:
                perID = params["id"]
                route = params["route"][params["next_route_space"]].values()[0]
                #speed = params["speed"]
                traci.person.add(perID, route[0], 0)
                traci.person.appendWalkingStage(perID, route, 0)
                traci.person.setSpeed(perID, 1)
                traci.person.appendWaitingStage(perID, 1)
            except Exception as e:
                raise e
            finally:
                pass
        if params["type"] == "vehicle":
            # NOT IMPL YET
            try:
                pass
            except Exception as e:
                raise e
            finally:
                pass
        return False

    def disapper(self, params):
        if params["type"] == "pedestrian":
            try:
                perID = params["id"]
                waiting = 1
                #print(traci.person.getStage(perID), traci.person.getNextEdge(perID))
                space_index = params["next_route_space"] - 1 if params["next_route_space"] else -1
                if not space_index == None:
                    print("AA", params["route"][space_index].values()[0][-1], params["road"])
                if traci.person.getNextEdge(perID) == "" and traci.person.getStage(perID) == waiting:
                    return True
                else:
                    return False
            except Exception as e:
                raise e
            finally:
                pass
        if params["type"] == "vehicle":
            # NOT IMPL YET
            try:
                pass
            except Exception as e:
                raise e
            finally:
                pass
        return False

    def simulator_init(self, params):
        if params["type"] == "SUMO":
            try:
                traci.init(port=int(params["port"]), label=params["sim_id"])
            except Exception as e:
                raise e
            finally:
                pass

    def departed(self, params):
        if params["type"] == "SUMO":
            try:
                return traci.simulation.getDepartedIDList()
            except Exception as e:
                raise e
            finally:
                pass

    def arrived(self, params):
        if params["type"] == "SUMO":
            try:
                return traci.simulation.getArrivedIDList()
            except Exception as e:
                raise e
            finally:
                pass

    def simulation_step(self, params):
        if params["type"] == "SUMO":
            try:
                return traci.simulationStep()
            except Exception as e:
                raise e
            finally:
                pass

    def simulator_switch(self, params):
        if params["type"] == "SUMO":
            try:
                traci.switch(params["id"])
            except Exception as e:
                raise e
            finally:
                pass

    def simulator_close(self, params):
        if params["type"] == "SUMO":
            try:
                traci.close()
            except Exception as e:
                raise e
            finally:
                pass

    def change_destination_from_geo(self, params):
        ret = None
        if params["type"] == "SUMO":
            try:
                ret = traci.simulation.convertRoad(params["lng"], params["lat"], True)
            except Exception as e:
                raise e
            finally:
                pass
        return ret

    def test_api(self, params):
        if params["type"] == "pedestrian":
            try:
                perID = params["id"]
                #print("AAAA", traci.person.getLanePosition(perID))
            except Exception as e:
                raise e
            finally:
                pass
        pass
        print(traci.simulation.getArrivedIDList())


    def __sample_api(self, params):
        if params["type"] == "pedestrian":
            try:
                pass
            except Exception as e:
                raise e
            finally:
                pass
        if params["type"] == "vehicle":
            try:
                pass
            except Exception as e:
                raise e
            finally:
                pass

#    def get_information(self, params):
#        parameters = {}
#        parameters["type"] = params["type"]
#        if params["type"] == "pedestrian":
#            try:
#                perID = params["id"]
#                parameters["road"] = traci.person.getRoadID(perID)
#                parameters["position"] = traci.person.getLanePosition(perID)
#                parameters["space_position"] = traci.person.getPosition(perID)
#                parameters["speed"] = traci.person.getSpeed(perID)
#            except Exception as e:
#                raise e
#            finally:
#                pass
#                #print("Call API: Get Object Information")
#        if params["type"] == "vehicle":
#            try:
#                vehID = params["id"]
#                route = traci.vehicle.getRoute(vehID)
#                parameters["road"] = traci.vehicle.getRoadID(vehID)
#                parameters["origin"] = route[0]
#                parameters["destination"] = route[-1]
#                parameters["space_position"] = traci.vehicle.getPosition(vehID)
#                parameters["position"] = traci.vehicle.getLanePosition(vehID)
#                parameters["speed"] = traci.vehicle.getSpeed(vehID)
#                parameters["angle"] = traci.vehicle.getAngle(vehID)
#            except Exception as e:
#                raise e
#            finally:
#                pass
#                #print("Call API: Get Object Information")
#        return parameters

API = SimulatorApi()

#def api_departed_list():
#    return traci.simulation.getDepartedIDList()
#
#def api_arrived_list():
#    return traci.simulation.getArrivedIDList()
#
#def api_simulation_step():
#    return traci.simulationStep()
#
#def api_get_position(vehID):
#    return traci.vehicle.getPosition(vehID)
#
#def api_get_destination(vehID):
#    return traci.vehicle.getRoute(vehID)[-1]
#
#def api_get_origin(vehID):
#    return traci.vehicle.getRoute(vehID)[0]
#
#
#def api_set_color(vehID, color):
#    traci.vehicle.setColor(vehID, color)
#
#def api_change_destination_from_geo(t_lng, t_lat):
#    return traci.simulation.convertRoad(t_lng, t_lat, True)
#
#def api_add_pedestrian(ped_id, route, position, speed):
#    traci.person.add(ped_id, route[0], position)
#    traci.person.appendWalkingStage(ped_id, route, 0.0)
#    traci.person.setSpeed(ped_id, 1)
#
#def api_get_pedestrian_info(ped_id):
#    edge = traci.person.getRoadID(ped_id)
#    pos = traci.person.getLanePosition(ped_id)
#    speed = traci.person.getSpeed(ped_id)
#    return (edge, pos, speed)
#
#def api_simulation_switch(sim_id):
#    traci.switch(sim_id)
#
