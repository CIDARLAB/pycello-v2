import json
import argparse
import matplotlib.pyplot as plt
import dnaplotlib as dpl
import pycello.netlist
import pycello.ucf
import pycello.dnaplotlib

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
        ucf = pycello.ucf.UCF(json.load(ucf_file))
    with open(args.netlist, 'r') as netlist_file:
        netlist = pycello.netlist.Netlist(json.load(netlist_file), ucf)

    designs = pycello.dnaplotlib.get_designs(netlist)

    fig = plt.figure(figsize=(5, len(designs)*1))

    h_frac = 1./len(designs)
    w_pad = 0.05
    for i, design in enumerate(designs):
        width = (1. - w_pad*(len(design) - 1))
        left = 0.0
        seq_len = 0
        for group in design:
            seq_len += group[-1]['end']
        for j, group in enumerate(design):
            w_frac = group[-1]['end'] / seq_len * width
            # Set up the axes for the genetic constructs
            rect = [left, i*h_frac, w_frac, h_frac]
            left += w_frac + w_pad
            ax = fig.add_axes(rect)

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
