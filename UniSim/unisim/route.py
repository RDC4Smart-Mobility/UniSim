# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

class Route(object):

    """
    args:
     route: String List
    """
    def __init__(self):
        self.route = []

    def specify(self, route, sims):
        ret = []
        ary = [None for i in range(len(route))]
        for sim in sims:
            for (index, edge) in enumerate(route):
                if sim.exist(edge):
                    ary[index] = sim.id()
        route = [r for (r, e) in zip(route, ary) if not e == None]

        ary = [e for e in ary if not e == None]
        space = None
        for (index, sim_id) in enumerate(ary):
            if not space == sim_id:
                space = sim_id
                ret.append( { space:[ route[index] ] } )
            else:
                ret[-1][space].append(route[index])
        return ret


if __name__ == "__main__":
    pass
