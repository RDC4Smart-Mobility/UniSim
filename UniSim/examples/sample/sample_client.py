# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import sys
import socket
from contextlib import closing

from unisim import BaseClient

class Client(BaseClient):
    def interpreter(self):
        pass

    def event_handler(self, info):
        if info["edges"][-1] in ("p1en", "p2en", "p3en"):
            if info["road"] in ("res1", "res2", "res3"):
                self._cmd = "get_parking"
                return True

if __name__ == '__main__':
    pass
    Client("", 4001).run('get_parking')
