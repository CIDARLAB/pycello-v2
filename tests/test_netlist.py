from .context import pycello
import pycello.netlist
import pycello.target_data
import json
import unittest

__author__ = 'Timothy S. Jones <jonests@bu.edu>, Densmore Lab, BU'
__license__ = 'GPL3'


class TestNetlist(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        path = "examples/Cello-UCF/files/v2/ucf/Eco/Eco1C1G1T1.UCF.json"
        with open(path) as fp:
            j = json.load(fp)
            cls.ucf = pycello.target_data.TargetDataFile(j)
        path = "examples/and_outputNetlist.json"
        with open(path) as netlist_file:
            cls.netlist_json = json.load(netlist_file)

    def test_netlist(self):
        pycello.netlist.Netlist(self.netlist_json)

    def test_netlist_dereference(self):
        netlist = pycello.netlist.Netlist(self.netlist_json)
        netlist.dereference()
        for edge in netlist.edges:
            self.assertIsInstance(edge.src, pycello.netlist.Node)

    def test_netlist_node_json(self):
        netlist = pycello.netlist.Netlist(self.netlist_json)
        node = netlist.nodes[0]
        encoder = pycello.netlist.NodeEncoder
        dump = json.dumps(node, cls=encoder, indent=4)
        reference = '{\n    "name": "a",\n    "nodeType": "PRIMARY_INPUT",\n    "partitionID": -1,\n    "deviceName": "LacI_sensor"\n}'
        self.assertEqual(dump, reference)

    def test_netlist_edge_json(self):
        netlist = pycello.netlist.Netlist(self.netlist_json)
        edge = netlist.edges[0]
        encoder = pycello.netlist.EdgeEncoder
        dump = json.dumps(edge, cls=encoder, indent=4)
        reference = '{\n    "name": "$n5_0",\n    "src": "$49",\n    "dst": "$50"\n}'
        self.assertEqual(dump, reference)

    def test_dereferenced_netlist_edge_json(self):
        netlist = pycello.netlist.Netlist(self.netlist_json)
        edge = netlist.edges[0]
        encoder = pycello.netlist.EdgeEncoder
        dump = json.dumps(edge, cls=encoder, indent=4)
        reference = '{\n    "name": "$n5_0",\n    "src": "$49",\n    "dst": "$50"\n}'
        self.assertEqual(dump, reference)

    def test_ucf_logiccircuit(self):
        with open('examples/0x78_A000_logic_circuit.txt') as lc_file:
            lc_text = lc_file.readlines()
        netlist = pycello.netlist.Netlist.fromLogicCircuit(lc_text)
        nodes = set([node.name for node in netlist.nodes])
        self.assertTrue("E1_BetI" in nodes, "Incorrect nodes.")


if __name__ == '__main__':
    unittest.main()
