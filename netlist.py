__author__  = 'Timothy S. Jones <jonests@bu.edu>, Densmore Lab, BU'
__license__ = 'GPL3'

def get_unit(node,placement):
    for unit in placement.units:
        if unit.node == node:
            return unit

class Unit:

    def __init__(self):
        self.parts = []

    @property
    def parts(self):
        return self.__parts

    @parts.setter
    def parts(self,parts):
        self.__parts = parts

    @property
    def node(self):
        return self.__node

    @node.setter
    def node(self,node):
        self.__node = node

    @property
    def sequence(self):
        sequence = ""
        for part in self.parts:
            sequence += part.sequence
        return sequence

class PartInstance:

    def __init__(self,part):
        self.part = part
        self.flux = 0.0
        self.color = 'black'

    @property
    def part(self):
        return self.__part

    @part.setter
    def part(self,part):
        self.__part = part

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self,color):
        self.__color = color
        
    @property
    def flux(self):
        return self.__flux

    @flux.setter
    def flux(self,flux):
        self.__flux = flux

class Placement:

    def __init__(self):
        self.units = []

    @property
    def units(self):
        return self.__units

    @units.setter
    def units(self,units):
        self.__units = units

class Edge:

    def __init__(self,edge):
        self.name = edge['name']

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self,name):
        self.__name = name

    @property
    def src(self):
        return self.__src

    @src.setter
    def src(self,src):
        self.__src = src

    @property
    def dst(self):
        return self.__dst

    @dst.setter
    def dst(self,dst):
        self.__dst = dst

class Node:

    def __init__(self,node,ucf):
        self.name = node['name']
        self.gate = ucf.gate(node['gateType'])
        self.type = node['nodeType']

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self,name):
        self.__name = name

    @property
    def gate(self):
        return self.__gate

    @gate.setter
    def gate(self,gate):
        self.__gate = gate

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self,type):
        self.__type = type

class Netlist:

    def __init__(self,netlist,ucf):
        self.nodes = []
        self.edges = []
        self.placements = []
        for node in netlist['nodes']:
            self.nodes.append(Node(node,ucf))
        for edge in netlist['edges']:
            e = Edge(edge)
            e.src = self.node(edge['src'])
            e.dst = self.node(edge['dst'])
            self.edges.append(e)
        for i in range(len(netlist['nodes'][0]['placements'])):
            placement = Placement()
            for j in range(len(self.nodes)):
                placement.units.append(Unit())
            self.placements.append(placement)
        for node in netlist['nodes']:
            for i,placement in enumerate(node['placements']):
                unit = self.placements[i].units[placement['position']-1]
                unit.node = self.node(node['name'])
                for component in placement['components']:
                    part = ucf.part(component)
                    gate = ucf.gate(component)
                    if (part):
                        instance = PartInstance(part)
                        unit.parts.append(instance)
                    if (gate):
                        for part in gate.parts:
                            instance = PartInstance(part)
                            unit.parts.append(instance)
                # unit.parts = placement['parts']

    @property
    def nodes(self):
        return self.__nodes

    @nodes.setter
    def nodes(self,nodes):
        self.__nodes = nodes

    def node(self,name):
        for node in self.nodes:
            if node.name == name:
                return node

    @property
    def edges(self):
        return self.__edges

    @edges.setter
    def edges(self,edges):
        self.__edges = edges

    @property
    def placements(self):
        return self.__placements

    @placements.setter
    def placements(self,placements):
        self.__placements = placements
