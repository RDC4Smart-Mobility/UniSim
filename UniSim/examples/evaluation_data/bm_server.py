# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import sys

from random import random

from unisim import BaseServer

class BenchmarkServer(BaseServer):
    
    def deal_msg(self, sock, msg, readfds):
        if len(msg) == 0:
            sock.close()
            readfds.remove(sock)

        elif msg:
            sock.send(msg)
        
        else:
            print(msg)


if __name__ == '__main__':
    BenchmarkServer("", 4001).run()
