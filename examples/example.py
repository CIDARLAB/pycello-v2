import pycello.netlist
import pycello.ucf

import json

with open('Eco1C1G1T1-synbiohub.UCF.json') as ucf_file:
    ucf_json = json.load(ucf_file)

with open('and_outputNetlist.json') as netlist_file:
    netlist_json = json.load(netlist_file)

ucf = pycello.ucf.UCF(ucf_json)
netlist = pycello.netlist.Netlist(netlist_json, ucf)

nodes = [node.name for node in netlist.nodes]
edges = [(edge.src.name, edge.dst.name) for edge in netlist.edges]

print("nodes: %s\n" % nodes)
print("edges: %s\n" % edges)
print("number of placements: %d\n" % len(netlist.placements))

for i, placement in enumerate(netlist.placements):
    print("placement %d" % i)
    print("number of sequences/plasmids: %d" % len(placement.groups))
    for j, group in enumerate(placement.groups):
        print("\tsequence/plasmid: %d" % j)
        print("\ttranscriptional units: %d" % len(group.components))
        for k, component in enumerate(group.components):
            print("\t\tcomponent: %s" % component.name)
    print()
