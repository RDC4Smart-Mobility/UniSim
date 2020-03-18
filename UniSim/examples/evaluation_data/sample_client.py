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
        if info["edges"][0] == info["origin"]:
            self._cmd = info["destination"]
            return True

if __name__ == '__main__':
    pass
