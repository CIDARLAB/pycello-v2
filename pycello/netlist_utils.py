from pycello.netlist import Component, Node, Netlist, Placement
from pycello.target_data import Gate, Part
import sympy

__author__ = 'Timothy S. Jones <jonests@bu.edu>, Densmore Lab, BU'
__license__ = 'GPL3'


def get_upstream_nodes(node: Node, netlist: Netlist):
    """Get the nodes connected as inputs to the given node in the netlist.

    Parameters
    ----------
    node : pycello.netlist.Node
    netlist : pycello.netlist.Netlist

    """
    upstream = []
    for edge in netlist.edges:
        if edge.dst == node:
            upstream.append(edge.src)
    return upstream


def get_upstream_node(promoter: Part, node: Node, netlist: Netlist):
    """Get the node with a given promoter connected as input to the given node.

    Parameters
    ----------
    promoter : pycello.ucf.Part
    node : pycello.netlist.Node
    netlist : pycello.netlist.Netlist

    """
    for upstream in get_upstream_nodes(node, netlist):
        gate = upstream.gate
        if gate.promoter == promoter:
            return upstream


def get_cds(component: Component):
    """Get the coding sequence in a given component.

    Parameters
    ----------
    component : pycello.netlist.Component

    Notes
    -----
    If more than one coding sequence is present, only the first in the
    `component` will be returned.

    """
    for part_instance in component.parts:
        if part_instance.part.type == 'cds':
            return part_instance


def get_ribozyme(component: Component):
    """Get the ribozyme in a given component.

    Parameters
    ----------
    component : pycello.netlist.Component

    Notes
    -----
    If more than one ribozyme is present, only the first in the
    `component` will be returned.

    """
    for part_instance in component.parts:
        if part_instance.part.type == 'ribozyme':
            return part_instance.part


def get_components(node: Node, placement: Placement):
    """Get the components in a placement corresponding to a given netlist node.

    Parameters
    ----------
    node : pycello.netlist.Node
    placement : pycello.netlist.Placement

    """
    components = []
    for group in placement.groups:
        for component in group.components:
            if component.node == node:
                components.append(component)
    return components


def evaluate_equation(gate: Gate, variables: dict):
    """Evaluate a gate's response function with supplied variables.

    Parameters
    ----------
    gate : pycello.ucf.Gate
    variables: dict

    """
    param_str = ""
    for param in gate.parameters.keys():
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
    expr = sympy.simplify(gate.equation)

    subs = []
    for param in param_syms:
        subs += ((param, gate.parameters[param.name]),)
    for var in var_syms:
        subs += ((var, variables[var.name]),)

    return expr.subs(subs)
