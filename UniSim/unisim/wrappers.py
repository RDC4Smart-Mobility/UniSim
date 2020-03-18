# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import socket
from contextlib import closing

class BaseClient(object):
    def __init__(self, addr, port):
        self._addr = addr
        self._port = port
        self._cmd = ""
        self._res = ""

    def operate_application(self, cmd):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        with closing(sock):
            sock.connect( (self._addr, self._port) )
            sock.send( str(cmd) )
            self._res = sock.recv(1024)

    def send_information(self, info):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        with closing(sock):
            sock.connect( (self._addr, self._port) )
            sock.send( str(info) )
            #self._res = sock.recv(1024)

    def interpreter(self):
        pass

    def event_handler(self):
        pass

    def get_cmd(self):
        return self._cmd

    def get_result(self):
        return self._res

    def run(self):
        self.operate_application(self._cmd)
        self.interpreter()

import socket
import select

import random

class BaseServer(object):
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self.backlog = 10
        self.bufsize = 4096

    def deal_msg(self, sock, msg, readfds):
        pass

    def run(self):
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        readfds = set([server_sock])
        try:
            #server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_sock.bind( (self._host, self._port) )
            server_sock.listen(self.backlog)

            while True:
                rready, wready, xready = select.select(readfds, [], [])
                for sock in rready:
                    if sock is server_sock:
                        conn, address = server_sock.accept()
                        readfds.add(conn)
                    else:
                        msg = sock.recv(self.bufsize)
                        self.deal_msg(sock, msg, readfds)

        finally:
            for sock in readfds:
                sock.close()
        return


import urllib
import urllib2
import json

class BaseCallApi(object):

    def __init__(self):
        self.url = "http://localhost:3000/"

    def operate_application(self, cmd):
        pass

    def interpreter(self):
        pass

    def event_handler(self):
        pass

    def get_method(self, url):
        return json.load(urllib2.urlopen(url))

    def _call_api(self, params):
        parameters = {}
        
        for index in params:
            if index == "url":
                continue
            if index == "method":
                continue
            if index == "parameters":
                for key in params["parameters"]:
                    parameters[key] = params["parameters"][key]
                continue
            parameters[index] = params[index]

        if (not params.has_key("method")) or params["method"] == "GET":
            if parameters:
                params["url"] += "?" + urllib.urlencode(parameters)
            self.response = self.get_method(params["url"])
        elif params["method"] == "POST":
            pass
        else:
            pass

    def call_api(self, params):
        if not params:
            return False
        return self._call_api(params)

    def run(self):
        self.operate_application(self._cmd)
        self.interpreter()

    def example(self, params={}):
        params["url"] = self.url + "points/"
        params["method"] = "GET"
        return self.call_api(params)


