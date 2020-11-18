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
          _              _       _
         | |            | |     | |
 ___  ___| |__   ___  __| |_   _| | ___
/ __|/ __| '_ \ / _ \/ _` | | | | |/ _ \
\__ \ (__| | | |  __/ (_| | |_| | |  __/
|___/\___|_| |_|\___|\__,_|\__,_|_|\___|

Generates lora transmission schedules for a network.

Once you have a node configuration, you can generate the
transmission schedule from which you can then evaluate the network
performance. The schedule is independent of the topology. The schedule
and topology are need in the evaluation step.

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
    parser.add_argument('-d', '--datadir', default='data',
                        help='Path to the output file.')    
    parser.add_argument('-o', '--output_filename', default='schedule.csv',
                        help='Name of the csv output schedule file to (over)write.')
    parser.add_argument('--overwrite', default=False,
                        help="Overwrite existing schedule file.")
    # parser.add_argument("--show", default=False, action='store_true',
    #                     help='Use matplotlib to plot topology.')
    parser.add_argument('type', nargs='?',
                        help="""How nodes transmit, for mixed networks use custom.
                        Periodic sends one message every interval with a small jitter.
                        Random sends one message every interval at a random time in each interval.
                        Custom reads a csv file with a row for each node.
                        """,
                        default='periodic',
                        choices=['periodic', 'random', 'custom'])
    parser.add_argument('-p', 'period', type=int, default=60*1000,
                        help="Period for transmission in milliseconds (ms).")
    parser.add_argument('-j', 'jitter', type=int, default=300,
                        help="Jitter for transmission in milliseconds (ms).")
    parser.add_argument('-e', 'end', type=int, default=10*60*1000,
                        help="End simulation time in milliseconds (ms).")
    args = parser.parse_args()


if __name__=="__main__": main()
