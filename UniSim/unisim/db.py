# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

# import sqlite3
import apsw # It is possible to operation across threads

import uuid
from datetime import datetime
from .agents import MobileAgent

class DB(object):

    def __init__(self):
        self.latest = 0
        self.retry = 3
        # self.dbpath = datetime.now().strftime("%Y-%m-%d-%H:%M:%S") + ".db"

    def connect(self):
        if self.dbpath:
            # self.conn = sqlite3.connect(self.dbpath)
            # self.cursor = self.conn.cursor()
            self.conn = apsw.Connection(self.dbpath)
            self.conn.setbusytimeout(3000) # keep retrying (ms)
            self.cursor = self.conn.cursor()

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def init_table(self):
        try:
            self.cursor.execute("BEGIN TRANSACTION;")
            sql = u"""
            CREATE TABLE master(
                tick INTEGER PRIMARY KEY AUTOINCREMENT,
                status CHAR(38)
            );
            """
            # self.conn.execute(sql) # sqlite3
            self.cursor.execute(sql)
        except Exception as e:
            print(e)
            self.cursor.execute("ROLLBACK;")
        else:
            self.cursor.execute("COMMIT;")

    def store(self, tick, objects):
        try:
            # insert tick/uuid into master table
            status_uuid = str(uuid.uuid4())
            self.cursor.execute("BEGIN TRANSACTION;")
            sql = u"""
            INSERT INTO master VALUES (?, ?);
            """
            self.cursor.execute(sql, (tick, status_uuid))

            # create table from status uuid
            sql = u"""
            CREATE TABLE "status_%s"(
                tick INTEGER,
                id CHAR(32),
                vehID CHAR(32),
                speed REAL,
                angle REAL,
                lng REAL,
                lat REAL,
                FOREIGN KEY(tick) REFERENCES master(tick)
            );
            """ % (status_uuid)
            # self.conn.execute(sql) # sqlite3
            self.cursor.execute(sql)

            # insert object data into status table
            for e in objects:
                sql = u"""
                INSERT INTO "status_%s" VALUES (%s, "%s", "%s", %s, %s, %s, %s);
                """ % (status_uuid,
                        tick,
                        e.id(),
                        e.object_information()["id"],
                        e.object_information()["speed"],
                        e.object_information()["angle"],
                        e.object_information()["lng"],
                        e.object_information()["lat"]
                        )
                self.cursor.execute(sql)
        except apsw.BusyError as e:
            print(e + ": rollback")
            # if self.conn.in_transaction: self.cursor.execute("ROLLBACK;")
            self.cursor.execute("ROLLBACK;")
        else:
            self.cursor.execute("COMMIT;")


    def resolved_status_from_tick(self, tick): # search tableID from tick
        sql = u"""
        SELECT * FROM master WHERE tick=%s;
        """ % (tick)
        self.cursor.execute(sql)
        res_tick, res_status_id = self.cursor.fetchone()
        return res_status_id

    def get_vehicle(self, tick, vehID): # /ticks/<tick>/vehicles/<vehID>, return <object>
        try:
            self.cursor.execute("BEGIN TRANSACTION;")
            tableID = self.resolved_status_from_tick(tick)
            sql = u"""
            SELECT * FROM "status_%s" where vehID = "%s";
            """ % (tableID, vehID)
            self.cursor.execute(sql)
            veh = self.cursor.fetchone()
            vehicle = {}
            # veh["tick"] = veh[0]
            vehicle["agentID"] = veh[1]
            vehicle["vehID"] = veh[2]
            vehicle["speed"] = veh[3]
            vehicle["angle"] = veh[4]
            vehicle["lng"] = veh[5]
            vehicle["lat"] = veh[6]
        except apsw.BusyError as e:
            print(e)
            self.cursor.execute("ROLLBACK;")
        else:
            self.cursor.execute("COMMIT;")
            return vehicle

    def get_vehicles(self, tick): # /ticks/<tick>/vehicles, return <list>
        try:
            self.cursor.execute("BEGIN TRANSACTION;")
            tableID = self.resolved_status_from_tick(tick)
            sql = u"""
            SELECT * FROM "status_%s";
            """ % (tableID)
            self.cursor.execute(sql)
            
            vehicles = []
            for veh in self.cursor:
                vehicle = {}
                # veh["tick"] = row2[0]
                vehicle["agentID"] = veh[1]
                vehicle["vehID"] = veh[2]
                vehicle["speed"] = veh[3]
                vehicle["angle"] = veh[4]
                vehicle["lng"] = veh[5]
                vehicle["lat"] = veh[6]
                vehicles.append(vehicle) 
        except apsw.BusyError as e:
            print(e)
            self.cursor.execute("ROLLBACK;")
        else:
            self.cursor.execute("COMMIT;")
            return vehicles

    def get_all(self): # /ticks, return <list>
        try:
            self.cursor.execute("BEGIN TRANSACTION;")
            tables = {}
            sql = u"""
            SELECT * FROM master;
            """
            self.cursor.execute(sql)
            for table in self.cursor:
                tables[table[0]] = table[1] # table: dictionary(key: tick, value: tableID)

            ticks = []
            for key in tables.keys(): # get information each tick
                tick = {}
                sql = u"""
                SELECT * FROM "status_%s";
                """ % (tables[key])
                self.cursor.execute(sql)

                vehicles = []
                for veh in self.cursor:
                    vehicle = {}
                    # veh["tick"] = row2[0]
                    vehicle["agentID"] = veh[1]
                    vehicle["vehID"] = veh[2]
                    vehicle["speed"] = veh[3]
                    vehicle["angle"] = veh[4]
                    vehicle["lng"] = veh[5]
                    vehicle["lat"] = veh[6]
                    vehicles.append(vehicle)
                tick["tick"] = key
                tick["vehicles"] = vehicles
                ticks.append(tick)
        except apsw.BusyError as e:
            print(e)
            self.cursor.execute("ROLLBACK;")
        else:
            self.cursor.execute("COMMIT;")
            return ticks

if __name__ == "__main__":
    db = DB()
    db.connect()
    db.init_table()
    db.store(1, [])
    db.store(2, [])
    db.resolved_status_from_tick(1)
    db.resolved_status_from_tick(2)
    db.disconnect()
