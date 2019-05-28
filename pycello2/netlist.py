__author__ = 'Timothy S. Jones <jonests@bu.edu>, Densmore Lab, BU'
__license__ = 'GPL3'


class Node:

    def __init__(self, node, ucf):
        self.name = node['name']
        self.gate = ucf.gate(node['gateType'])
        self.type = node['nodeType']

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def gate(self):
        return self.__gate

    @gate.setter
    def gate(self, gate):
        self.__gate = gate

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, type):
        self.__type = type


class Edge:

    def __init__(self, edge):
        self.name = edge['name']

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def src(self):
        return self.__src

    @src.setter
    def src(self, src):
        self.__src = src

    @property
    def dst(self):
        return self.__dst

    @dst.setter
    def dst(self, dst):
        self.__dst = dst


class Placement:

    def __init__(self):
        self.groups = []

    @property
    def groups(self):
        return self.__groups

    @groups.setter
    def groups(self, groups):
        self.__groups = groups


class PlacementGroup:

    def __init__(self):
        self.components = []

    @property
    def components(self):
        return self.__components

    @components.setter
    def components(self, components):
        self.__components = components

    @property
    def sequence(self):
        sequence = ""
        for component in self.components:
            sequence += component.sequence
        return sequence


class Component:

    def __init__(self):
        self.parts = []

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def parts(self):
        return self.__parts

    @parts.setter
    def parts(self, parts):
        self.__parts = parts

    @property
    def node(self):
        return self.__node

    @node.setter
    def node(self, node):
        self.__node = node

    @property
    def sequence(self):
        sequence = ""
        for part in self.parts:
            sequence += part.part.sequence
        return sequence


class PartInstance:

    def __init__(self, part):
        self.part = part
        self.flux = 0.0
        self.color = 'black'

    @property
    def part(self):
        return self.__part

    @part.setter
    def part(self, part):
        self.__part = part

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, color):
        self.__color = color

    @property
    def flux(self):
        return self.__flux

    @flux.setter
    def flux(self, flux):
        self.__flux = flux


class Netlist:

    def __init__(self, netlist, ucf):
        self.nodes = []
        self.edges = []
        self.placements = []

        for node in netlist['nodes']:
            self.nodes.append(Node(node, ucf))
        for edge in netlist['edges']:
            e = Edge(edge)
            e.src = self.node(edge['src'])
            e.dst = self.node(edge['dst'])
            self.edges.append(e)
        for placement in netlist['placements']:
            p = Placement()
            self.placements.append(p)
            for group in placement:
                g = PlacementGroup()
                p.groups.append(g)
                g.name = group['name']
                for component in group['components']:
                    c = Component()
                    g.components.append(c)
                    c.name = component['name']
                    c.node = self.node(component['node'])
                    for obj in component['parts']:
                        part = ucf.part(obj)
                        gate = ucf.gate(obj)
                        if (part):
                            instance = PartInstance(part)
                            c.parts.append(instance)
                        if (gate):
                            for part in gate.parts:
                                instance = PartInstance(part)
                                c.parts.append(instance)

    @property
    def nodes(self):
        return self.__nodes

    @nodes.setter
    def nodes(self, nodes):
        self.__nodes = nodes

    def node(self, name):
        for node in self.nodes:
            if node.name == name:
                return node

    @property
    def edges(self):
        return self.__edges

    @edges.setter
    def edges(self, edges):
        self.__edges = edges

    @property
    def placements(self):
        return self.__placements

    @placements.setter
    def placements(self, placements):
        self.__placements = placements


def get_upstream_node(part, node: Node, netlist: Netlist):
    """Get the node immediately upstream of a given node, with gate having
    promoter 'part'."""
    for upstream in get_upstream_nodes(node, netlist):
        gate = upstream.gate
        if gate.promoter == part:
            return upstream


def get_cds(component: Component):
    """Get the coding sequence in a given component."""
    for part_instance in component.parts:
        if part_instance.part.type == 'cds':
            return part_instance


def get_ribozyme(component: Component):
    """Get the ribozyme sequence in a given component."""
    for part_instance in component.parts:
        if part_instance.part.type == 'ribozyme':
            return part_instance.part


def get_component(node: Node, placement: Placement):
    """Get the component in a placement group corresponding to a given node."""
    for group in placement.groups:
        for component in group.components:
            if component.node == node:
                return component


def get_upstream_nodes(node: Node, netlist: Netlist):
    """Get the nodes immediately upstream of a given node."""
    upstream = []
    for edge in netlist.edges:
        if edge.dst == node:
            upstream.append(edge.src)
    return upstream
