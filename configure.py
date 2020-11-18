#!/usr/bin/env python3
"""
loraWanSim: lora network simulator

copyright 2020 Alan Marchiori <amm042@bucknell.edu>

--------------------------------------------------------------------------------
loraWanSim splits network simulation into four parts:
 1. Topology generation (topology.py)
 2. Node configuration (configure.py)
 2. Node & gateway transmission schedules (schedule.py)
 3. Performance evaluation (evaluate.py)

The goal of this separation is to simplify the simulator and make various
analyses easier by keeping detailed intermediate files. We focus on LoraWAN
class A devices using acknowledgments as much of the previous work uses
unacknowledged transmissions. Future work will include class B (and C) nodes.

This lora simulator is inspired by LoRaSim by Thiemo Voigt and Martin Bor.

  Do LoRa Low-Power Wide-Area Networks Scale? Martin Bor, Utz Roedig,
  Thiemo Voigt and Juan Alonso, MSWiM '16, http://dx.doi.org/10.1145/2988287.2989163
--------------------------------------------------------------------------------
                  __ _
                 / _(_)
  ___ ___  _ __ | |_ _  __ _ _   _ _ __ ___
 / __/ _ \| '_ \|  _| |/ _` | | | | '__/ _ \
| (_| (_) | | | | | | | (_| | |_| | | |  __/
 \___\___/|_| |_|_| |_|\__, |\__,_|_|  \___|
                        __/ |
                       |___/

Configures nodes in a simulated lora network.

Once you have a network configured, you can generate the
transmission schedule from which you can then evaluate the network
performance. The configuration and schedule are independent of the topology.
The schedule and topology are need in the evaluation step.

--------------------------------------------------------------------------------
"""
# Command Line Interface Creation Kit
# https://click.palletsprojects.com
import click

import pandas as pd
import os.path
import utils.io as io
from pprint import pprint
from utils.exception import ApplicationException
#
# def main ():
    # parser = argparse.ArgumentParser(
    #     description=__doc__,
    #     formatter_class=HelpFormatter)
    #
    # parser.add_argument('nodes', default=1, nargs='?', type=int,
    #                     help="Number of nodes to generate.")
    # parser.add_argument('-d', '--datadir', default='data',
    #                     help='Path to the output file.')
    # parser.add_argument('-o', '--output_filename', default='network.csv',
    #                     help='Name of the csv configuration file to (over)write.')
    # parser.add_argument('--loraclass', default='a',
    #                     choices=['a', 'b', 'c'],
    #                     help='Lora node class.')
    # parser.add_argument('--lorasf', default='7',
    #                     choices=range(6, 13),
    #                     help='Lora node spreading factor(sf).')
    # parser.add_argument('--lorasf', default='7',
    #                     choices=range(6, 13),
    #                     help='Lora node spreading factor(sf).')
    # parser.add_argument('--overwrite', default=False,
    #                     help="Overwrite existing configuration (True) file or append (False).")
    # # parser.add_argument("--show", default=False, action='store_true',
    # #                     help='Use matplotlib to plot topology.')
    # parser.add_argument('type', nargs='?',
    #                     help="""How the nodes transmit.
    #                     Periodic sends one message every interval with a small jitter.
    #                     Random sends one message every interval at a random time in each interval.
    #                     """,
    #                     default='periodic',
    #                     choices=['periodic', 'random'])
    # parser.add_argument('-p', 'period', type=int, default=60*1000,
    #                     help="Period for transmission in milliseconds (ms).")
    # parser.add_argument('-j', 'jitter', type=int, default=300,
    #                     help="Jitter for transmission in milliseconds (ms).")
    #
    # args = parser.parse_args()
    #
    # output_pathfile = os.path.join(args.datadir, args.output_filename)
    #

@click.group()
@click.option('--datadir', default='./data',
              help='Path to configuration.')
@click.option('--filename', default='network.csv',
              help='Network configuration filename.')
@click.option('-c', '--country', default='US',
              help='Country channel plan to use (only US currently supported).')
@click.pass_context
def main(ctx, datadir, filename, country):
    """loraWanSim: lora network simulator

    copyright 2020 Alan Marchiori <amm042@bucknell.edu>

    Configures nodes in a simulated lora network.

    Once you have a network configured, you can generate the
    transmission schedule from which you can then evaluate the network
    performance. The configuration and schedule are independent of the topology.
    The schedule and topology are need in the evaluation step.
    """
    # setup context only
    config = io.load_config(datadir, filename)
    ctx.obj = {'datadir': datadir, 'filename': filename, 'config': config}

    if country=='US':
        import lorastd.us902
        ctx.obj['channels'] = lorastd.us902.us902()

@main.command(short_help='List configuration items')
@click.pass_context
def ls(ctx):
    "Lists node configuration."
    pprint(ctx.obj['config'])


@main.command(short_help='Add node(s) to a network configuration.')
@click.pass_context
@click.option('-n', '--nodes', default=1,
                help='How many (identical) nodes to add.')
@click.option('--nodeid', default=None,
                help='Node id, Default (None) auto increments.')
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
def add(ctx, nodes, nodeid, channels, tx_schedule, payload_size, period, jitter):
    "Add a node to a network configuration."

    pass

@main.command(short_help='Remove node(s) from a network configuration.')
@click.pass_context
def rm(ctx):
    pass

main.add_command(ls)
main.add_command(add)
main.add_command(rm)

if __name__=="__main__":
    try:
        main(obj={})
    except ApplicationException as x:
        print(x)
