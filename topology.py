#!/usr/bin/env python3
"""
loraWanSim: lora network simulator

copyright 2020 Alan Marchiori <amm042@bucknell.edu>

--------------------------------------------------------------------------------
loraWanSim splits network simulation into three parts:
 1. Topology generation (topology.py)
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
 _                    _
| |                  | |
| |_ ___  _ __   ___ | | ___   __ _ _   _
| __/ _ \| '_ \ / _ \| |/ _ \ / _` | | | |
| || (_) | |_) | (_) | | (_) | (_| | |_| |
 \__\___/| .__/ \___/|_|\___/ \__, |\__, |
         | |                   __/ | __/ |
         |_|                  |___/ |___/

Generates lora network topologies to be used in lora network simulations.

Node positions are specified in 2-dimensional coordinates in units of meters
from the origin, where the gateway node is located.

Currently only a single gateway node is supported.
--------------------------------------------------------------------------------
"""

import argparse
from utils.io import write_topo
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
    parser.add_argument('-d', '--datadir', default='data',
                        help='Path to the output file.')
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

    nodes = [(0, 0, 0)] # list of nodes (nodeId, Xpos, Ypos)
    # node 0 is the gateway, located at the origin.

    if args.place == 'sunflower':
        from utils.sunflower import sunflower
        nodes += list(sunflower(args.nodes, radius=args.max_distance//2))
    elif args.place == 'grid':
        from utils.grid import grid
        nodes += list(grid(args.nodes, radius=args.max_distance//2))
    elif args.place == 'random':
        from utils.rand import rand
        nodes += list(rand(args.nodes, radius=args.max_distance//2))

    # write the output
    data = pd.DataFrame(nodes, columns=['nodeid', 'x', 'y'])

    # remove raw nodes, work on data only from here.
    del nodes
    output_pathfile = os.path.join(args.datadir, args.output_filename)
    if os.path.exists(output_pathfile) and not args.overwrite:
        existing = pd.read_csv(output_pathfile)
        maxnode = max(existing['nodeid'])

        # copy slice out to a new dataframe.
        newdata = pd.DataFrame.copy(data[1:])
        # renumber generated node ids to follow
        newdata['nodeid'] = newdata['nodeid'] + maxnode
        # ignore first row, it's the gateway, we don't want two.
        data = pd.concat([existing, newdata], axis=0)
    data.to_csv(output_pathfile, index=False)

    if args.show:
        import matplotlib.pyplot as plt
        fig = plt.figure(figsize=(4,4))
        ax = fig.add_subplot(111)

        data[0:1].plot.scatter(x='x', y='y', ax=ax, c='green')
        data[1:].plot.scatter(x='x', y='y', ax=ax, c='blue')

        maxcircle = plt.Circle((0,0), args.max_distance//2,
                               color='r', lw=2, alpha=0.8,
                               fill=False)
        ax.add_artist(maxcircle)
        ax.set_xlim((1.1*-args.max_distance//2, 1.1*args.max_distance//2))
        ax.set_ylim((1.1*-args.max_distance//2, 1.1*args.max_distance//2))

        plt.tight_layout()
        plt.show()


if __name__=="__main__": main()
