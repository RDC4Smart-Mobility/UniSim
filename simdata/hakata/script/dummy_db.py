# -*- coding: utf-8 -*-
from unisim import DB

class DummyDB(DB):

    def connect(self):
        pass
    
    def disconnect(self):
        pass
    
    def init_table(self):
        pass
    
    def store(self, tick, objects):
        pass
