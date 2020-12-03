#!/usr/bin/env python3
"""
loraWanSim: lora network simulator

copyright 2020 Alan Marchiori <amm042@bucknell.edu>

See README for important background info.
--------------------------------------------------------------------------------
                             __
                            / _|
  __ _  _ __   _ __    ___ | |_   __ _
 / _` || '_ \ | '_ \  / __||  _| / _` |
| (_| || |_) || |_) || (__ | |  | (_| |
 \__,_|| .__/ | .__/  \___||_|   \__, |
       | |    | |                 __/ |
       |_|    |_|                |___/

Configures applications in a simulated lora network. The configuration includes
the application logic, transmission and acknowledgment schedules.

https://docs.python.org/3.7/library/importlib.html#module-importlib
--------------------------------------------------------------------------------
"""
# Command Line Interface Creation Kit
# https://click.palletsprojects.com
import click

import pandas as pd
import os.path
from utils.jsonfile import loadjson, savejson
from pprint import pprint
from utils.exception import ApplicationException
import json

@click.group()
@click.option('--datadir', default='./data',
              help='Path to configuration info.')
@click.option('--filename', default='appconfig.json',
              help='Application configuration filename.')
@click.pass_context
def main(ctx, datadir, filename):
    """loraWanSim: lora network simulator

    copyright 2020 Alan Marchiori <amm042@bucknell.edu>

    Configures applications in a simulated lora network. The configuration includes
    the application logic, transmission and acknowledgment schedules.
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
    "List configured applications."
    pprint(ctx.obj['config'])

@main.command()
@click.pass_context
@click.argument('appname', required = True)
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
def mk(ctx, appname, tx_schedule, payload_size, period, jitter):
    "Add an APPNAME application."
    # channels are a string that is a json-encoded list
    channels = json.loads(channels)
    assert type(channels) == list
    node = {
        'tx_schedule': tx_schedule,
        'payload_size': payload_size,
        'period': period,
        'jitter': jitter
    }
    if appname in ctx.obj['config']:
        print ("Node name \"{}\" already exists.".format(appname))
    else:
        ctx.obj['config'][appname] = node
        savejson(ctx.obj['pathfile'], ctx.obj['config'])

@main.command()
@click.pass_context
@click.argument('appname')
def rm(ctx, appname):
    """Remove an APPNAME application."""
    if name in ctx.obj['config']:
        del ctx.obj['config'][appname]
        savejson(ctx.obj['pathfile'], ctx.obj['config'])
        print("Success.")
    else:
        print("App name \"{}\" not found in config.".format(appname))

main.add_command(ls)
main.add_command(mk)
main.add_command(rm)

if __name__=="__main__":
    try:
        main(obj={})
    except ApplicationException as x:
        print(x)
