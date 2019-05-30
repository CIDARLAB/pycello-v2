from . import netlist as pycello2_netlist
import sympy

__author__ = 'Timothy S. Jones <jonests@bu.edu>, Densmore Lab, BU'
__license__ = 'GPL3'


def get_upstream_node(part,
                      node: pycello2_netlist.Node,
                      netlist: pycello2_netlist.Netlist):
    """Get the node immediately upstream of a given node, with gate having
    promoter 'part'."""
    for upstream in get_upstream_nodes(node, netlist):
        gate = upstream.gate
        if gate.promoter == part:
            return upstream


def get_cds(component: pycello2_netlist.Component):
    """Get the coding sequence in a given component."""
    for part_instance in component.parts:
        if part_instance.part.type == 'cds':
            return part_instance


def get_ribozyme(component: pycello2_netlist.Component):
    """Get the ribozyme sequence in a given component."""
    for part_instance in component.parts:
        if part_instance.part.type == 'ribozyme':
            return part_instance.part


def get_components(node: pycello2_netlist.Node, placement: pycello2_netlist.Placement):
    """Get the components in a placement that correspond to a given netlist node."""
    components = []
    for group in placement.groups:
        for component in group.components:
            if component.node == node:
                components.append(component)
    return components


def get_upstream_nodes(node: pycello2_netlist.Node, netlist: pycello2_netlist.Netlist):
    """Get the nodes immediately upstream of a given node."""
    upstream = []
    for edge in netlist.edges:
        if edge.dst == node:
            upstream.append(edge.src)
    return upstream


def evaluate_equation(gate, variables):
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
