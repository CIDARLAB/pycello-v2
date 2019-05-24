import numpy as np
import matplotlib.pyplot as plt
import argparse
import json
import csv
import sympy
import dnaplotlib as dpl

import pycello2.netlist
import pycello2.dnaplotlib
import pycello2.ucf

__author__ = 'Timothy S. Jones <jonests@bu.edu>, Densmore Lab, BU'
__license__ = 'GPL3'


def main():
    parser = argparse.ArgumentParser(
        description="Plot RNAseq profile from predicted RPU."
    )
    parser.add_argument("--ucf", "-u",
                        required=True, help="UCF file.", metavar="FILE")
    parser.add_argument("--activity-table", "-a", dest="activity",
                        required=True, help="Activity table.", metavar="FILE")
    parser.add_argument("--logic-table", "-l", dest="logic",
                        required=True, help="Logic table.", metavar="FILE")
    parser.add_argument("--netlist", "-n",
                        required=True, help="Netlist.", metavar="FILE")
    parser.add_argument("--output", "-o",
                        required=False, help="Output file.", metavar="FILE")
    args = parser.parse_args()

    activity = []
    logic = []
    with open(args.ucf, 'r') as ucf_file:
        ucf = pycello2.ucf.UCF(json.load(ucf_file))
    with open(args.activity, 'r') as activity_file:
        activity_reader = csv.reader(activity_file)
        for row in activity_reader:
            activity.append(row)
    with open(args.logic, 'r') as logic_file:
        logic_reader = csv.reader(logic_file)
        for row in logic_reader:
            logic.append(row)
    with open(args.netlist, 'r') as netlist_file:
        netlist = pycello2.netlist.Netlist(json.load(netlist_file), ucf)

    designs = pycello2.dnaplotlib.get_designs(netlist)

    placement = netlist.placements[0].groups[0]

    def get_node_logic(node):
        for row in logic:
            if row[0] == node.name:
                return row[1:]

    def get_node_activity(node):
        for row in activity:
            if row[0] == node.name:
                return row[1:]

    def evaluate_equation(node, variables):
        param_str = ""
        for param in node.gate.parameters.keys():
            param_str += param + " "
        param_syms = sympy.symbols(param_str)
        if type(param_syms) is not tuple:
            param_syms = (param_syms,)
        var_str = ""
        for var in variables.keys():
            var_str += var
        var_syms = sympy.symbols(var_str)
        if type(var_syms) is not tuple:
            var_syms = (var_syms,)
        expr = sympy.simplify(node.gate.equation)

        subs = []
        for param in param_syms:
            subs += ((param, node.gate.parameters[param.name]),)
        for var in var_syms:
            subs += ((var, variables[var.name]),)

        return expr.subs(subs)

    num_plots = len(logic[0]) - 1

    fig = plt.figure()
    gs = fig.add_gridspec(num_plots + 1, 1)

    components = []
    for component in placement.components:
        if component.node.type != 'PRIMARY_INPUT':
            components.append(component)
    ax = []

    for row in range(num_plots):
        if row == 0:
            ax.append(fig.add_subplot(gs[row]))
        else:
            ax.append(fig.add_subplot(gs[row], sharex=ax[0], sharey=ax[0]))

        profile = []
        temp = []
        for component in components:
            for part in component.parts:
                temp.append(1)
                profile.append(100)
        while (np.max(np.abs(np.array(profile) - np.array(temp))) > 1e-3):
            temp = profile.copy()
            profile = []
            for i, component in enumerate(components):
                for j, part_instance in enumerate(component.parts):
                    # offset to which we add the flux (readthrough, upstream promoter flux)
                    if j == 0 and i > 0:
                        offset = components[i-1].parts[-1].flux
                    elif j > 0:
                        offset = component.parts[j-1].flux
                    else:
                        offset = 0.0

                    if part_instance.part.type == 'promoter':
                        upstream = pycello2.netlist.get_upstream_node(part_instance.part,component.node,netlist)
                        if upstream.type == 'PRIMARY_INPUT':
                            delta_flux = float(get_node_activity(upstream)[row])
                        else:
                            input_flux = pycello2.netlist.get_component(upstream, placement).parts[-2].flux
                            delta_flux = evaluate_equation(upstream, {'x': input_flux})
                        part_instance.flux = pycello2.netlist.get_ribozyme(component).efficiency * delta_flux + offset
                    if part_instance.part.type == 'ribozyme':
                        part_instance.flux = offset / get_ribozyme(component).efficiency
                    if part_instance.part.type in ('cds','rbs'):
                        part_instance.flux = offset
                    if part_instance.part.type == 'terminator':
                        part_instance.flux = offset/part_instance.part.strength

                    profile.append(part_instance.flux)

        ax[row].set_xticks([])
        ax[row].set_yscale('log')
        # ax[row].set_yscale('log')
        x = []
        y = []
        last_x = 0
        last_y = 1e-8
        for i, component in enumerate(components):
            x.append([])
            y.append([])
            # cello_gate_activity = float(get_node_activity(component.node)[row])

            for j, part_instance in enumerate(component.parts):
                if j == 0:
                    initial_x = last_x
                    initial_y = last_y
                else:
                    initial_x = x[-1][-1]
                    initial_y = y[-1][-1]

                if part_instance.part.type == 'terminator':
                    x[-1].append(initial_x)
                    x[-1].append(initial_x + int(0.5*len(part_instance.part.sequence)))
                    x[-1].append(initial_x + int(0.5*len(part_instance.part.sequence)))
                    x[-1].append(initial_x + len(part_instance.part.sequence))
                    y[-1].append(initial_y)
                    y[-1].append(initial_y)
                    y[-1].append(part_instance.flux)
                    y[-1].append(part_instance.flux)
                elif part_instance.part.type == 'promoter':
                    x[-1].append(initial_x)
                    x[-1].append(initial_x + len(part_instance.part.sequence))
                    x[-1].append(initial_x + len(part_instance.part.sequence))
                    y[-1].append(initial_y)
                    y[-1].append(initial_y)
                    y[-1].append(part_instance.flux)
                elif part_instance.part.type == 'ribozyme':
                    x[-1].append(initial_x)
                    x[-1].append(initial_x + 7)
                    x[-1].append(initial_x + 7)
                    x[-1].append(initial_x + len(part_instance.part.sequence))
                    y[-1].append(initial_y)
                    y[-1].append(initial_y)
                    y[-1].append(part_instance.flux)
                    y[-1].append(part_instance.flux)
                else:
                    x[-1].append(initial_x)
                    x[-1].append(initial_x + len(part_instance.part.sequence))
                    y[-1].append(part_instance.flux)
                    y[-1].append(part_instance.flux)

            if i == 0:
                pre_x = []
                pre_y = []
            else:
                pre_x = [last_x, ]
                pre_y = [last_y, ]

            x[-1] = pre_x + x[-1]
            y[-1] = pre_y + y[-1]

            last_x = x[-1][-1]
            last_y = y[-1][-1]

        for i, component in enumerate(components):
            color = 'blue' if get_node_logic(component.node)[row] == 'false' else 'red'
            color = 'black'
            ax[row].plot(x[i], y[i], '-', color=color)

    plt.xlim(x[0][0], x[-1][-1])
    plt.subplots_adjust(hspace=0.0)

    # Set up the axes for the genetic constructs
    ax_dna = fig.add_subplot(gs[num_plots])

    # Create the DNAplotlib renderer
    dr = dpl.DNARenderer()

    # Redender the DNA to axis
    start, end = dr.renderDNA(ax_dna, designs[0][0], dr.trace_part_renderers())
    ax_dna.set_xlim([start, end])
    ax_dna.set_ylim([-5, 10])
    ax_dna.set_aspect('auto')
    ax_dna.set_xticks([])
    ax_dna.set_yticks([])
    ax_dna.axis('off')

    if (args.output):
        out_file = args.output
    else:
        out_file = 'out'
        plt.savefig(out_file + '.png')


if __name__ == "__main__":
    main()
