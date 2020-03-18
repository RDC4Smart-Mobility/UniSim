# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

from unisim.RESTserver import app, Flask_DB
from datetime import datetime

import sys

if __name__ == "__main__":
    Flask_DB.dbpath = sys.argv[1]
    Flask_DB.connect()
    app.run(host='0.0.0.0') # host='0.0.0.0': allow connecting from external client
