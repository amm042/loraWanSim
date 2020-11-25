"""
why doesn't python json have this? Idk.
"""
import json
from collections import OrderedDict
def loadjson(pathfile, default={}):
    try:
        with open(pathfile, 'r') as fp:
            return json.load(fp, object_pairs_hook=OrderedDict)
    except FileNotFoundError:
        return default

def savejson(pathfile, obj):
    with open(pathfile, 'w') as fp:
        return json.dump(obj,fp, indent=2, sort_keys=False)
