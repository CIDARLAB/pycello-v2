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


def get_node_logic(node, logic):
    for row in logic:
        if row[0] == node.name:
            return row[1:]


def get_node_activity(node, activity):
    for row in activity:
        if row[0] == node.name:
            return row[1:]


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

    # dnaplotlib specifications
    designs = pycello2.dnaplotlib.get_designs(netlist)

    placement = netlist.placements[0]

    num_plots = len(logic[0])

    widths = [len(group.sequence) for group in placement.groups]

    fig = plt.figure(figsize=(np.sum(widths)/650, num_plots))
    gs = fig.add_gridspec(num_plots, len(placement.groups), width_ratios=widths)

    axes = []

    for row in range(num_plots - 1):
        axes_row = []
        axes.append(axes_row)
        for col, group in enumerate(placement.groups):
            sharex = axes[row - 1][col] if row > 0 else None
            sharey = axes[0][0] if (row != 0 or col != 0) else None
            ax = fig.add_subplot(gs[row, col], sharex=sharex, sharey=sharey)
            axes_row.append(ax)

            profile = []
            temp = []
            for component in group.components:
                for part in component.parts:
                    temp.append(1.0)
                    profile.append(100.0)
            while (np.max(np.abs(np.array(profile) - np.array(temp))) > 1e-3):
                temp = profile.copy()
                profile = []
                for i, component in enumerate(group.components):
                    for j, part_instance in enumerate(component.parts):
                        # offset to which we add the flux (readthrough, upstream promoter flux)
                        if j == 0 and i > 0:
                            offset = group.components[i-1].parts[-1].flux
                        elif j > 0:
                            offset = component.parts[j-1].flux
                        else:
                            offset = 0.0

                        if part_instance.part.type == 'promoter':
                            upstream_node = pycello2.netlist.get_upstream_node(part_instance.part, component.node, netlist)
                            if upstream_node.type == 'PRIMARY_INPUT':
                                delta_flux = float(get_node_activity(upstream_node, activity)[row])
                            else:
                                upstream_components = pycello2.netlist.get_components(upstream_node, placement)
                                input_flux = 0.0
                                for upstream_component in upstream_components:
                                    input_flux += upstream_component.parts[-2].flux
                                delta_flux = evaluate_equation(upstream_node, {'x': input_flux})
                            part_instance.flux = pycello2.netlist.get_ribozyme(component).efficiency * delta_flux + offset
                        if part_instance.part.type == 'ribozyme':
                            part_instance.flux = offset / pycello2.netlist.get_ribozyme(component).efficiency
                        if part_instance.part.type in ('cds', 'rbs'):
                            part_instance.flux = offset
                        if part_instance.part.type == 'terminator':
                            part_instance.flux = offset / part_instance.part.strength

                        profile.append(part_instance.flux)

            ax.set_xticks([])
            ax.set_yscale('log')
            if col > 0:
                plt.setp(ax.get_yticklabels(), visible=False)
                ax.tick_params(axis=u'both', which=u'both', length=0)

            x = []
            y = []
            last_x = 0
            last_y = 1e-6

            for i, component in enumerate(group.components):
                x.append([])
                y.append([])

                for j, part_instance in enumerate(component.parts):
                    if j == 0:
                        initial_x = last_x
                        initial_y = last_y
                    else:
                        initial_x = x[-1][-1]
                        initial_y = y[-1][-1]

                    if part_instance.part.type == 'terminator':
                        x[-1].append(initial_x)
                        x[-1].append(initial_x + int(0.5*len(part_instance.part. sequence)))
                        x[-1].append(initial_x + int(0.5*len(part_instance.part. sequence)))
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

            for i, component in enumerate(group.components):
                color = 'blue' if get_node_logic(component.node,logic)[row] == 'false' else 'red'
                color = 'black'
                ax.plot(x[i], y[i], '-', color=color)

            ax.set_xlim(x[0][0], x[-1][-1])

    for i, group in enumerate(placement.groups):
        ax_dna = fig.add_subplot(gs[-1, i])
        inv = ax_dna.transData.inverted()
        design = designs[0][i]
        for part in design:
            if part['type'] == 'Promoter':
                part['opts']['x_extent'] = np.sum(widths)/30
            if part['type'] == 'Terminator':
                part['opts']['x_extent'] = np.sum(widths)/100
            if part['type'] == 'CDS':
                part['opts']['arrowhead_length'] = np.sum(widths)/100

        dr = dpl.DNARenderer()
        start, end = dr.renderDNA(ax_dna, design, dr.trace_part_renderers())
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
    plt.tight_layout()
    plt.subplots_adjust(hspace=0.0, wspace=0.1)
    plt.savefig(out_file + '.png', bbox_to_inches='tight')


if __name__ == "__main__":
    main()
