#!/usr/bin/env python3
"""
loraWanSim: lora network simulator

copyright 2020 Alan Marchiori <amm042@bucknell.edu>

See README for important background info.
--------------------------------------------------------------------------------
 _                             __
| |                           / _|
| |  ___   _ __   __ _   ___ | |_   __ _
| | / _ \ | '__| / _` | / __||  _| / _` |
| || (_) || |   | (_| || (__ | |  | (_| |
|_| \___/ |_|    \__,_| \___||_|   \__, |
                                    __/ |
                                   |___/

Configures lora radio parameters for nodes in a simulated lora network. The
configuration includes the complete Lora configuration (channel/sf/bw/nc/etc)
for a node.
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

@click.group()
@click.option('--datadir', default='./data',
              help='Path to configuration info.')
@click.option('--filename', default='nodeconfig.json',
              help='Node configuration filename.')
@click.pass_context
def main(ctx, datadir, filename):
    """loraWanSim: lora network simulator

    copyright 2020 Alan Marchiori <amm042@bucknell.edu>

    Configures lora radio parameters for nodes in a simulated lora network. The
    configuration includes the complete Lora configuration (channel/sf/bw/nc/etc)
    for a node.
    """
    # setup context only

    ctx.obj = {
        'datadir': datadir,
        'filename': filename,
        'pathfile': os.path.join(datadir, filename),
        'config': None}
    ctx.obj['config'] = loadjson(ctx.obj['pathfile'], default={})

@main.command()
@click.pass_context
def ls(ctx):
    "Lists lora configurations."
    pprint(ctx.obj['config'])


@main.command()
@click.pass_context
@click.argument('loraname', required = True)
@click.option('-r', '--region', default='US',
              help='Regional channel plan to use (only US currently supported).')
@click.option('-u', '--upstream', default='[8,9,10,11,12,13,14,15]',
                help='JSON-style list of channel numbers for upstream transmissions')
@click.option('-d', '--downstream', default='[0,1,2,3,4,5,6,7]',
                help='JSON-style list of channel numbers for downstream transmissions')
def mk(ctx, loraname, region, upstream, downstream):
    "Add a LORANAME lora configuration."
    # channels are a string that is a json-encoded list
    channels = json.loads(channels)
    assert type(channels) == list
    node = {
        'region': region,
        'upstream': upstream,
        'downstream': downstream
    }
    if loraname in ctx.obj['config']:
        print ("Node name \"{}\" already exists.".format(loraname))
    else:
        ctx.obj['config'][loraname] = node
        savejson(ctx.obj['pathfile'], ctx.obj['config'])

@main.command()
@click.pass_context
@click.argument('loraname')
def rm(ctx, loraname):
    """Remove a LORANAME lora configuration."""
    if name in ctx.obj['config']:
        del ctx.obj['config'][loraname]
        savejson(ctx.obj['pathfile'], ctx.obj['config'])
        print("Success.")
    else:
        print("Lora name \"{}\" not found in config.".format(loraname))

main.add_command(ls)
main.add_command(mk)
main.add_command(rm)

if __name__=="__main__":
    try:
        main(obj={})
    except ApplicationException as x:
        print(x)
