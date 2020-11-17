#!/usr/bin/env python3
"""
loraWanSim: lora network simulator

copyright 2020 Alan Marchiori <amm042@bucknell.edu>

--------------------------------------------------------------------------------
loraWanSim splits network simulation into three parts:
 1. Topology generation
 2. Node & gateway transmission schedules
 3. Performance evaluation

The goal of this separation is to simplify the simulator and make various
analyses easier by keeping detailed intermediate files. We focus on LoraWAN
class A devices using acknowledgments as much of the previous work uses
unacknowledged transmissions. Future work will include class B (and C) nodes.

This lora simulator is inspired by LoRaSim by Thiemo Voigt and Martin Bor.

  Do LoRa Low-Power Wide-Area Networks Scale? Martin Bor, Utz Roedig,
  Thiemo Voigt and Juan Alonso, MSWiM '16, http://dx.doi.org/10.1145/2988287.2989163
--------------------------------------------------------------------------------
          _              _       _
         | |            | |     | |
 ___  ___| |__   ___  __| |_   _| | ___
/ __|/ __| '_ \ / _ \/ _` | | | | |/ _ \
\__ \ (__| | | |  __/ (_| | |_| | |  __/
|___/\___|_| |_|\___|\__,_|\__,_|_|\___|

Generates lora transmission schedules for a network.

Once you have a topology and a schedule, you can evaluate the network
performance. The schedule is independent of the topology.

We focus on class A acknowledge messages but also support unacknowledged
class A messages.
--------------------------------------------------------------------------------
"""

import argparse
import pandas as pd
import os.path

class HelpFormatter(argparse.ArgumentDefaultsHelpFormatter,
                    argparse.RawDescriptionHelpFormatter):
    "mix defaults and raw description."
    pass

def main ():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=HelpFormatter)

    parser.add_argument('nodes', default=10, nargs='?', type=int,
                        help="Number of nodes to generate.")
    parser.add_argument('-o', '--output_filename', default='topo.csv',
                        help='Name of the csv output topology file to (over)write.')
    parser.add_argument('--overwrite', default=False,
                        help="Overwrite existing topology file.")
    parser.add_argument("--show", default=False, action='store_true',
                        help='Use matplotlib to plot topology.')
    parser.add_argument('place', nargs='?',
                        help='How to place nodes.',
                        default='sunflower',
                        choices=['sunflower', 'grid', 'random'])
    parser.add_argument('max_distance',default=8000, type=int, nargs='?',
                        help='Maximum distance from the gateway (meters).')

    args = parser.parse_args()


if __name__=="__main__": main()
