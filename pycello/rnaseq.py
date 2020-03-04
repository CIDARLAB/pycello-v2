import numpy as np
import argparse
import json
import csv
import logging

import pycello.netlist
import pycello.dnaplotlib
import pycello.ucf
import pycello.utils

__author__ = 'Timothy S. Jones <jonests@bu.edu>, Densmore Lab, BU'
__license__ = 'GPL3'


BASAL_TRANSCRIPTION = 1e-6
TOLERANCE = 1e-5


def strtobool(s):
    """Convert a string representation of a boolean to a boolean."""
    if s.lower() == "true":
        return True
    if s.lower() == "false":
        return False


def placement_rnaseq(netlist, placement, activity):
    """Get the RNAseq profile for a given placement in a netlist."""
    profile = {p: 100.0 for g in placement.groups for c in g.components for p in c.parts}
    temp = {p: 1.0 for g in placement.groups for c in g.components for p in c.parts}

    while (np.max(np.abs(np.array(list(profile.values())) - np.array(list(temp.values())))) > TOLERANCE):
        temp = profile.copy()
        profile = {}
        for i, group in enumerate(placement.groups):
            for j, component in enumerate(group.components):
                for k, part_instance in enumerate(component.parts):
                    # offset to which we add the flux
                    # (readthrough, upstream promoter flux)
                    if k == 0 and j > 0:
                        offset = profile[group.components[j-1].parts[-1]]
                    elif k > 0:
                        offset = profile[component.parts[k-1]]
                    else:
                        offset = 0.0

                    if part_instance.part.type == 'promoter':
                        upstream_node = pycello.utils.get_upstream_node(part_instance.part, component.node, netlist)
                        if upstream_node.type == 'PRIMARY_INPUT':
                            delta_flux = activity[upstream_node.name][0]
                        else:
                            upstream_components = pycello.utils.get_components(upstream_node, placement)
                            input_flux = 0.0
                            for upstream_component in upstream_components:
                                input_flux += profile[pycello.utils.get_cds(upstream_component)]
                            delta_flux = pycello.utils.evaluate_equation(upstream_node.gate, {'x': input_flux})
                        profile[part_instance] = pycello.utils.get_ribozyme(component).efficiency * delta_flux + offset
                    if part_instance.part.type == 'ribozyme':
                        profile[part_instance] = offset / pycello.utils.get_ribozyme(component).efficiency
                    if part_instance.part.type in ('cds', 'rbs'):
                        profile[part_instance] = offset
                    if part_instance.part.type == 'terminator':
                        profile[part_instance] = offset / part_instance.part.strength

    return profile


def rnaseq(ucf, netlist, activity, logic):
    """Get the RNAseq profile from a given netlist."""
    rtn = {}

    dt = np.dtype([(row[0], np.bool) for row in logic])
    logic = np.array([[strtobool(k) for k in row[1:]] for row in logic]).T
    logic = np.array([tuple(row) for row in logic], dtype=dt)

    dt = np.dtype([(row[0], np.float) for row in activity])
    activity = np.array([[float(k) for k in row[1:]] for row in activity]).T
    activity = np.array([tuple(row) for row in activity], dtype=dt)

    if (activity.shape != logic.shape):
        raise ValueError("Activity and Logic arrays must have the same size.")
    for placement in netlist.placements:
        rtn[placement] = []
        for i in range(activity.shape[0]):
            rtn[placement].append(placement_rnaseq(netlist, placement, activity[i:i+1]))

    return rtn


def plot_rnaseq(rnaseq, designs):
    """Plot RNA-seq data.

    Parameters
    ----------
    rnaseq : list
        The json representation of the rnaseq data, as returned by `get_json`.

    """
    # for placement in rnaseq:

    # num_plots = logic.shape[0]
    # widths = [len(group.sequence) for i, group in enumerate(placement.groups) if i not in skip]
    pass


def get_json(rnaseq):
    """Get a json representation of the RNAseq profile."""
    rtn = []
    for placement in rnaseq.keys():
        x = []
        rtn.append(x)
        for state in rnaseq[placement]:
            y = []
            x.append(y)
            for part in state.keys():
                y.append({"name": part.part.name, "value": state[part]})
    return rtn


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Plot RNAseq profile from predicted RPU."
    )
    parser.add_argument("--ucf", "-u",
                        required=True, help="UCF file.", metavar="FILE")
    parser.add_argument("--activity-table", "-a", dest="activity",
                        required=True, help="Activity csv file.", metavar="FILE")
    parser.add_argument("--logic-table", "-l", dest="logic",
                        required=True, help="Logic csv file.", metavar="FILE")
    parser.add_argument("--netlist", "-n",
                        required=True, help="Netlist.", metavar="FILE")
    parser.add_argument("--output", "-o",
                        required=False, help="Output file.", metavar="FILE")
    parser.add_argument("--debug", "-d",
                        required=False, help="Debug.", action='store_true')
    args = parser.parse_args()

    activity = []
    logic = []
    with open(args.ucf, 'r') as ucf_fp:
        ucf = pycello.ucf.UCF(json.load(ucf_fp))
    with open(args.activity, 'r') as activity_fp:
        activity_reader = csv.reader(activity_fp)
        for row in activity_reader:
            activity.append(row)
    with open(args.logic, 'r') as logic_fp:
        logic_reader = csv.reader(logic_fp)
        for row in logic_reader:
            logic.append(row)
    with open(args.netlist, 'r') as netlist_fp:
        netlist = pycello.netlist.Netlist(json.load(netlist_fp), ucf)

    seq = rnaseq(ucf, netlist, activity, logic)
    data = get_json(seq)
