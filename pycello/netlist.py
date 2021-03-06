import re

__author__ = 'Timothy S. Jones <jonests@bu.edu>, Densmore Lab, BU'
__license__ = 'GPL3'


class Node:

    def __init__(self, node, ucf):
        self.name = node['name']
        self.type = node['nodeType']
        self.partition_id = node['partitionID']
        self.gate = ucf.gate(node['gateType'])

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, type):
        self.__type = type

    @property
    def partition_id(self):
        return self.__partition_id

    @partition_id.setter
    def partition_id(self, partition_id):
        self.__partition_id = partition_id

    @property
    def gate(self):
        return self.__gate

    @gate.setter
    def gate(self, gate):
        self.__gate = gate

    @property
    def json(self):
        rtn = {
            "name": self.name,
            "nodeType": self.type,
            "partitionID": self.partition_id,
            "gateType": self.gate.name
        }

        return rtn


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

    @property
    def json(self):
        rtn = {
            "name": self.name,
            "src": self.src.name,
            "dst": self.dst.name
        }

        return rtn


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
        self.name = netlist['name'] if 'name' in netlist else ""
        self.input_filename = netlist['inputFilename'] if 'inputFilename' in netlist else ""
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

    @classmethod
    def fromLogicCircuit(self, lc, ucf):
        netlist = {}
        netlist["name"] = "default"
        netlist["inputFilename"] = "default.v"
        netlist["nodes"] = []
        netlist["edges"] = []
        netlist["placements"] = []

        nodes = {}
        edges = []

        for line in lc:
            regex = r"^(OUTPUT_OR|OUTPUT|NOT|NOR|INPUT)\s+[01]+\s+(\w+)\s+(\d+)\s+(\(\d+(,\d+)*\))?"
            m = re.match(regex, line)
            if (m):
                node = {}
                node["name"] = m.group(2)
                if (m.group(1) in ["OUTPUT_OR", "OUTPUT"]):
                    node["nodeType"] = "PRIMARY_OUTPUT"
                    node["gateType"] = re.sub("^output_", "", m.group(2))
                    node["gateType"] += "_reporter"
                elif (m.group(1) == "INPUT"):
                    node["nodeType"] = "PRIMARY_INPUT"
                    node["gateType"] = re.sub("^input_", "", m.group(2))
                    if (node["gateType"] == "pBAD"):
                        node["gateType"] = "AraC_sensor"
                    if (node["gateType"] == "pTet"):
                        node["gateType"] = "TetR_sensor"
                    if (node["gateType"] == "pLuxStar"):
                        node["gateType"] = "LuxR_sensor"
                    if (node["gateType"] == "pTac"):
                        node["gateType"] = "LacI_sensor"
                else:
                    node["nodeType"] = m.group(1)
                    node["gateType"] = m.group(2)

                node["partitionID"] = -1

                nodes[m.group(3)] = node["name"]

                netlist["nodes"].append(node)

                if (m.group(4)):
                    inputs = m.group(4)
                    inputs = inputs.lstrip("(")
                    inputs = inputs.rstrip(")")
                    for dst in inputs.split(","):
                        edges.append((dst, m.group(3)))

        for edge in edges:
            netlist_edge = {}
            netlist_edge["name"] = nodes[edge[0]] + "_" + nodes[edge[1]]
            netlist_edge["src"] = nodes[edge[0]]
            netlist_edge["dst"] = nodes[edge[1]]
            netlist["edges"].append(netlist_edge)

        return Netlist(netlist, ucf)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def input_filename(self):
        return self.__input_filename

    @input_filename.setter
    def input_filename(self, input_filename):
        self.__input_filename = input_filename

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

    @property
    def json(self):
        rtn = {
            "name": self.name,
            "inputFilename": self.input_filename,
            "placements": [],
            "nodes": [],
            "edges": []
        }

        for placement in self.placements:
            pass
        for node in self.nodes:
            rtn['nodes'].append(node.json)
        for edge in self.edges:
            rtn['edges'].append(edge.json)

        return rtn
