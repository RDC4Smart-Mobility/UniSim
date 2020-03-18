# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import sqlite3
import matplotlib.pyplot as plt
import numpy as np


class Analyzer(object):

    def __init__(self, dbpath):
        self.dbpath = dbpath

    def connect(self):
        if self.dbpath:
            self.conn = sqlite3.connect(self.dbpath)
            self.cursor = self.conn.cursor()

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def in_rect(self, x, y, dx, dy):
        ret = []
        # Number of object in rect angle (x, y), (x + dx, y + dy)
        sql = u"""
            SELECT * FROM master;
        """
        self.cursor.execute(sql)
        for tick, status_id in self.cursor.fetchall():
        #res_tick, res_status_id = self.cursor.fetchone()
            sql = u"""
                select count(*) from "status_%s"
                where %s < lat and lat < %s
                and %s < lng and lng < %s;
            """ % (status_id, x, x + dx, y , y + dy)
            self.cursor.execute(sql)
            n = self.cursor.fetchone()[0]
            ret.append((tick, n))
        return ret

if __name__ == "__main__":
    ana = Analyzer("./sample.db")
    ana.connect()

    data = ana.in_rect(100, 0, 4000, 2000)
    x, y = zip(*data[:-1])
    plt.plot(x,y)
    plt.show()

    ana.disconnect()

