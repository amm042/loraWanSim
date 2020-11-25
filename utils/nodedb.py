"""
Helper class to access and update the node/json database.

This is intended to be used inside a context/with statement ie:

with nodedb() as nodes:
    pass

"""
import os.path
from utils.jsonfile import loadjson, savejson

class nodedb:
    "Wrapper for the node database."
    def __init__(self, datadir='.', filename='network.json'):
        self.pathfile = os.path.join(datadir, filename)
        self.db = None
    def __enter__(self):
        self.db = loadjson(self.pathfile, default=[{}])
    def __exit__(self, exc_type, exec_val, exec_tb):
        savejson(self.db, self.pathfile)
        self.db = None
