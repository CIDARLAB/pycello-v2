import json
import argparse
import matplotlib.pyplot as plt
import dnaplotlib as dpl
import pycello2.netlist
import pycello2.ucf
import pycello2.dnaplotlib

__author__ = 'Timothy S. Jones <jonests@bu.edu>, Densmore Lab, BU'
__license__ = 'GPL3'


def main():
    parser = argparse.ArgumentParser(
        description="Plot RNAseq profile from predicted RPU."
    )
    parser.add_argument("--ucf", "-u",
                        required=True, help="UCF file.", metavar="FILE")
    parser.add_argument("--netlist", "-n",
                        required=True, help="Netlist.", metavar="FILE")
    parser.add_argument("--output", "-o",
                        required=False, help="Output file.", metavar="FILE")
    args = parser.parse_args()

    with open(args.ucf, 'r') as ucf_file:
        ucf = pycello2.ucf.UCF(json.load(ucf_file))
    with open(args.netlist, 'r') as netlist_file:
        netlist = pycello2.netlist.Netlist(json.load(netlist_file), ucf)

    designs = pycello2.dnaplotlib.get_designs(netlist)

    fig = plt.figure()

    h_frac = 1./len(designs)
    for i, design in enumerate(designs):
        w_frac = 1./len(design)
        for j, group in enumerate(design):
            # Set up the axes for the genetic constructs
            ax = fig.add_axes([j*w_frac, i*h_frac, w_frac, h_frac])

            # Create the DNAplotlib renderer
            dr = dpl.DNARenderer()

            # Redender the DNA to axis
            start, end = dr.renderDNA(ax, group, dr.trace_part_renderers())
            ax.set_xlim([start, end])
            ax.set_ylim([-5, 10])
            ax.set_aspect('auto')
            ax.set_xticks([])
            ax.set_yticks([])
            ax.axis('off')

    if (args.output):
        out_file = args.output
    else:
        out_file = 'out'
        plt.savefig(out_file + '.png')


if __name__ == "__main__":
    main()
