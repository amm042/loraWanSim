#!/usr/bin/env python3
"""
loraWanSim: lora network simulator

copyright 2020 Alan Marchiori <amm042@bucknell.edu>

See README for important background info.
--------------------------------------------------------------------------------
              _                           _
             | |                         | |
 _ __    ___ | |_ __      __  ___   _ __ | | __
| '_ \  / _ \| __|\ \ /\ / / / _ \ | '__|| |/ /
| | | ||  __/| |_  \ V  V / | (_) || |   |   <
|_| |_| \___| \__|  \_/\_/   \___/ |_|   |_|\_\

Configures a lora network. This is the binding of topology node Id to
node type string.
--------------------------------------------------------------------------------
"""
# Command Line Interface Creation Kit
# https://click.palletsprojects.com
import click

import pandas as pd
import os.path
#import utils.io as io
from utils.jsonfile import loadjson, savejson
from pprint import pprint
from utils.exception import ApplicationException
import json
from collections import OrderedDict

@click.group()
@click.option('--datadir', default='./data',
              help='Path to configuration info.')
@click.option('--filename', default='netconfig.json',
              help='Network configuration filename.')
@click.pass_context
def main(ctx, datadir, filename):
    """loraWanSim: lora network simulator

    copyright 2020 Alan Marchiori <amm042@bucknell.edu>

    Configures a lora network. This is the binding of topology node_id to
    node type string.
    """
    # setup context only

    ctx.obj = {
        'datadir': datadir,
        'filename': filename,
        'pathfile': os.path.join(datadir, filename),
        'config': None}
    ctx.obj['config'] = loadjson(ctx.obj['pathfile'],
                                default=OrderedDict())

@main.command(short_help='List configured node types.')
@click.pass_context
def ls(ctx):
    "Lists network configuration."
    pprint(ctx.obj['config'])

@main.command(short_help='Makes a network configuration.')
@click.pass_context
@click.argument('nodeid', required = True, type=int)
@click.argument('name', required = True)
@click.option('-r', '--repeat', default = 1, type=int,
            help='Create REPEAT copies of node, incrementing node id by 1.')
@click.option('--node_filename', default='nodeconfig.json',
              help='Node configuration filename.')
def set(ctx, nodeid, name, repeat, node_filename):
    "Set NODEID to use NAME node configuration."

    # load nodes to validate name strings
    nfp = os.path.join(ctx.obj['datadir'], node_filename)
    cfg_nodes = loadjson(nfp)

    if name in cfg_nodes:
        for i in range(repeat):
            ctx.obj['config'][nodeid+i] = name
        savejson(ctx.obj['pathfile'], ctx.obj['config'])
    else:
        print("Failed: \"{}\" is not defined in {}".format(
            name, nfp
        ))

main.add_command(ls)
main.add_command(set)

if __name__=="__main__":
    try:
        main(obj={})
    except ApplicationException as x:
        print(x)
