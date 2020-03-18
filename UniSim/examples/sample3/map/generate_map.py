# coding: utf-8

import os, sys

def check_file_name(file):
    if isinstance(file, basestring):
        file = file
    elif is_pathlib_path(file):
        file = file.parent / file.name
    return file

import json
def get_information(file):
    maps = None
    connections = None
    if file.endswith(".json"):
        try:
            f = open(file, "r")
            info = json.load(f)
            maps = info["net"]
            connections = info["connections"]
        except Exception as e:
            raise Exception("Can't extract information.")
        finally:
            f.close()
    else:
        raise Exception("Not .json File")
    return maps, connections

from xml.dom import minidom
conns = None

def add_connections(maps, connections):
    for m in maps:
        doc = minidom.parse(m)
        junctions = doc.getElementsByTagName("junction")
        for junction in junctions:
            for index, conn in enumerate(connections):
                if any(junction.getAttribute("incLanes").startswith(c) for c in conn):
                    junction_id = junction.getAttribute("id")

                    ep_edge_id = "EP:" + junction_id
                    lane_id = ep_edge_id + "_0"
                    ep_junction_id = "EPJ:" + junction_id

                    #
                    conns[index].append(ep_junction_id)

                    # append edge , edge->lane
                    add_edge = doc.createElement("edge")
                    add_edge.setAttribute("id", ep_edge_id)
                    add_edge.setAttribute("from", junction_id)
                    add_edge.setAttribute("to", ep_junction_id)
                    add_edge.setAttribute("priority", "1")
                    # append lane
                    child_lane = doc.createElement("lane")
                    shape = junction.getAttribute("shape")
                    child_lane.setAttribute("id", lane_id)
                    child_lane.setAttribute("length", "0.1")
                    child_lane.setAttribute("width", "2.0")
                    child_lane.setAttribute("index", "0")
                    # pedestrian setting
                    child_lane.setAttribute("allow", "pedestrian")
                    child_lane.setAttribute("speed", "2.78")
                    #
                    child_lane.setAttribute("shape",shape)
                    add_edge.appendChild(child_lane)
                    # append junction, ToDo: Only append doc
                    clone_junction = junction.cloneNode(True)
                    clone_junction.setAttribute("id", ep_junction_id)

                    # Append section
                    junction.parentNode.appendChild(add_edge)
                    junction.parentNode.appendChild(clone_junction)

        # Write Phase
        with open(m.replace("net", "ext.net"), "w") as f:
            doc.writexml(f)


def generate_master_map(maps):
    doc = minidom.parseString("<net />")
    docs = map(minidom.parse, maps)
    for d in docs:
        for e in d.getElementsByTagName("net")[0].childNodes:
            if not e.nodeType in [e.TEXT_NODE]:
                doc.documentElement.appendChild(e)
    for index, c in enumerate(conns):
        edge = doc.createElement("edge")
        edge.setAttribute("id", "CONN:" + str(index))
        edge.setAttribute("from", c[0])
        edge.setAttribute("to", c[1])
        edge.setAttribute("priority", "1")
        lane = doc.createElement("lane")
        lane.setAttribute("id", "CONN:" + str(index) + "_0")
        lane.setAttribute("index", "0")
        lane.setAttribute("speed", "10")
        lane.setAttribute("length", "0.2")
        edge.appendChild(lane)
        doc.documentElement.appendChild(edge)
    #print(doc.toxml())
    # Generate Phase
    with open("master.xml", "w") as f:
        doc.writexml(f, '', ' '*4, '\n', encoding='UTF-8')

if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("json file not selected.")
        print("ex. python generate_map.py connections.json")
        exit()
    print("#-- Generating extend net file / master net file. --#")
    file = check_file_name(sys.argv[1])
    maps, connections = get_information(file)
    conns = [[] for i in connections]
    add_connections(maps, connections)
    generate_master_map(map(lambda x: x.replace("net", "ext.net"), maps))
