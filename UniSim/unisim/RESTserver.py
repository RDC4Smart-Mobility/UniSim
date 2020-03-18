# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

from .db import DB
from datetime import datetime

# import threading
import json
from flask import Flask, jsonify, request, url_for, abort, Response
# for using decorator
from functools import wraps

import sys

# Decolator for MIME Type Check
def consumes(content_type):
    def _consumes(function):
        @wraps(function)
        def __consumes(*args, **keywords):
            if request.headers['Content-Type'] != content_type:
                # status code 400 (Bad Request)
                abort(400)
            return function(*args, **keywords)
        return __consumes
    return _consumes

# Flask side
app = Flask(__name__)
Flask_DB = DB()


def dbstart(dbpath, port):
    Flask_DB.dbpath = dbpath
    Flask_DB.connect()
    app.run(host='0.0.0.0', port=port)

@app.route('/ticks', methods=['GET'])
def return_ticks():
    response = jsonify({"ticks": Flask_DB.get_all()})
    # status code 200 (OK)
    response.status_code = 200
    return response

@app.route('/ticks/<int:tick>', methods=['GET'])
def return_tick(tick):
    response = jsonify({
        "tick": tick,
        "vehicles": Flask_DB.get_vehicles(tick)
    })
    # status code 200 (OK)
    response.status_code = 200
    return response

@app.route('/ticks/<int:tick>/vehicles', methods=['GET'])
def return_vehicles(tick):
    response = jsonify({
        "vehicles": Flask_DB.get_vehicles(tick)
    })
    # status code 200 (OK)
    response.status_code = 200
    return response

@app.route('/ticks/<int:tick>/vehicles/<string:vehID>', methods=['GET'])
def information_vehicle(tick, vehID):
    response = jsonify(Flask_DB.get_vehicle(tick, vehID))
    # status code 200 (OK)
    response.status_code = 200
    return response

if __name__ == "__main__":
    Flask_DB.dbpath = sys.argv[1]
    Flask_DB.connect()
    app.run(host='0.0.0.0') # host='0.0.0.0': allow connecting from external client
