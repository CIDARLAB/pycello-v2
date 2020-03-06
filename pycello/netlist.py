import json
import re
from pycello.utils import find_by_name

__author__ = 'Timothy S. Jones <jonests@bu.edu>, Densmore Lab, BU'
__license__ = 'GPL3'


class NodeEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Node):
            return {
                "name": obj.name,
                "nodeType": obj.node_type,
                "partitionID": obj.partition_id,
                "deviceName": obj.device_name
            }
        return super(NodeEncoder, self).default(obj)


class Node:

    def __init__(self, node):
        self.name = node['name']
        self.node_type = node['nodeType']
        self.partition_id = node['partitionID']
        self.device_name = node['deviceName']

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def node_type(self):
        return self.__node_type

    @node_type.setter
    def node_type(self, node_type):
        self.__node_type = node_type

    @property
    def partition_id(self):
        return self.__partition_id

    @partition_id.setter
    def partition_id(self, partition_id):
        self.__partition_id = partition_id

    @property
    def device_name(self):
        return self.__device_name

    @device_name.setter
    def device_name(self, device_name):
        self.__device_name = device_name


class EdgeEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Edge):
            return {
                "name": obj.name,
                "src": obj.src.name if isinstance(obj.src, Node) else obj.src,
                "dst": obj.dst.name if isinstance(obj.dst, Node) else obj.dst
            }
        return super(EdgeEncoder, self).default(obj)


class Edge:

    def __init__(self, edge):
        self.name = edge["name"]
        self.src = edge["src"]
        self.dst = edge["dst"]

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

    def __init__(self, netlist):
        if "name" in netlist:
            self.name = netlist["name"]
        if "inputFilename" in netlist:
            self.input_filename = netlist["inputFilename"]
        self.nodes = []
        self.edges = []
        self.placements = []

        for node in netlist["nodes"]:
            self.nodes.append(Node(node))
        for edge in netlist["edges"]:
            self.edges.append(Edge(edge))

    def dereference(self):
        for edge in self.edges:
            edge.src = find_by_name(edge.src, self.nodes)
            edge.dst = find_by_name(edge.dst, self.nodes)
        # for placement in netlist["placements"]:
        #     p = Placement()
        #     self.placements.append(p)
        #     for group in placement:
        #         g = PlacementGroup()
        #         p.groups.append(g)
        #         g.name = group['name']
        #         for component in group['components']:
        #             c = Component()
        #             g.components.append(c)
        #             c.name = component['name']
        #             c.node = self.node(component['node'])
        #             for obj in component['parts']:
        #                 part = ucf.part(obj)
        #                 gate = ucf.gate(obj)
        #                 if (part):
        #                     instance = PartInstance(part)
        #                     c.parts.append(instance)
        #                 if (gate):
        #                     for part in gate.parts:
        #                         instance = PartInstance(part)
        #                         c.parts.append(instance)

    @classmethod
    def fromLogicCircuit(self, lc):
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
                    node["deviceName"] = re.sub("^output_", "", m.group(2))
                    node["deviceName"] += "_reporter"
                elif (m.group(1) == "INPUT"):
                    node["nodeType"] = "PRIMARY_INPUT"
                    node["deviceName"] = re.sub("^input_", "", m.group(2))
                    # if (node["deviceName"] == "pBAD"):
                    #     node["deviceName"] = "AraC_sensor"
                    # if (node["deviceName"] == "pTet"):
                    #     node["deviceName"] = "TetR_sensor"
                    # if (node["deviceName"] == "pLuxStar"):
                    #     node["deviceName"] = "LuxR_sensor"
                    # if (node["deviceName"] == "pTac"):
                    #     node["deviceName"] = "LacI_sensor"
                else:
                    node["nodeType"] = m.group(1)
                    node["deviceName"] = m.group(2)

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

        return Netlist(netlist)

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

    # @property
    # def json(self):
    #     rtn = {
    #         "name": self.name,
    #         "inputFilename": self.input_filename,
    #         "placements": [],
    #         "nodes": [],
    #         "edges": []
    #     }

    #     for placement in self.placements:
    #         pass
    #     for node in self.nodes:
    #         rtn['nodes'].append(node.json)
    #     for edge in self.edges:
    #         rtn['edges'].append(edge.json)

    #     return rtn
