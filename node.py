#!/usr/bin/env python3
"""
loraWanSim: lora network simulator

copyright 2020 Alan Marchiori <amm042@bucknell.edu>

See README for important background info.
--------------------------------------------------------------------------------
                   _
                  | |
 _ __    ___    __| |  ___
| '_ \  / _ \  / _` | / _ \
| | | || (_) || (_| ||  __/
|_| |_| \___/  \__,_| \___|

Configures nodes in a simulated lora network. The configuration includes the
complete Lora configuration (channel/sf/bw/nc/etc) for a node.
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

    Configures nodes in a simulated lora network. The configuration includes the
    complete Lora configuration (channel/sf/bw/nc/etc) for a node.
    """
    # setup context only

    ctx.obj = {
        'datadir': datadir,
        'filename': filename,
        'pathfile': os.path.join(datadir, filename),
        'config': None}
    ctx.obj['config'] = loadjson(ctx.obj['pathfile'], default={})

@main.command(short_help='List configured node types.')
@click.pass_context
def ls(ctx):
    "Lists node configuration."
    pprint(ctx.obj['config'])


@main.command(short_help='Makes a node configuration.')
@click.pass_context
@click.argument('name', required = True)
@click.option('-c', '--country', default='US',
              help='Country channel plan to use (only US currently supported).')
@click.option('-c', '--channels', default='[8,9,10,11,12,13,14,15]',
                help='JSON-style list of channel numbers for transmissions')
@click.option('-t', '--tx_schedule', default='periodic',
                type=click.Choice(['periodic', 'random']),
                help="""How the nodes transmit.
                Periodic sends one message every interval with a defined jitter.
                Random sends one message every interval at a random time in each interval.
                """)
@click.option('-s', '--payload_size', default=12,
                help="Payload size in bytes")
@click.option('-p','--period', default = 60*1000,
                help="Period for transmission in milliseconds (ms).")
@click.option('-j','--jitter', default = 300,
                help="Jitter for transmission in milliseconds (ms).")
def mk(ctx, name, country, channels, tx_schedule, payload_size, period, jitter):
    "Add a NAME node configuration."
    # channels are a string that is a json-encoded list
    channels = json.loads(channels)
    assert type(channels) == list
    node = {
        'country': country,
        'channels': channels,
        'tx_schedule': tx_schedule,
        'payload_size': payload_size,
        'period': period,
        'jitter': jitter
    }
    if name in ctx.obj['config']:
        print ("Node name \"{}\" already exists.".format(name))
    else:
        ctx.obj['config'][name] = node
        savejson(ctx.obj['pathfile'], ctx.obj['config'])

@main.command(short_help='Remove node from a network configuration.')
@click.pass_context
@click.argument('name')
def rm(ctx, name):
    """Remove a NAME node configuration."""
    if name in ctx.obj['config']:
        del ctx.obj['config'][name]
        savejson(ctx.obj['pathfile'], ctx.obj['config'])
        print("Success.")
    else:
        print("Node name \"{}\" not found in config.".format(name))

main.add_command(ls)
main.add_command(mk)
main.add_command(rm)

if __name__=="__main__":
    try:
        main(obj={})
    except ApplicationException as x:
        print(x)
