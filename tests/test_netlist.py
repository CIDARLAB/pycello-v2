from .context import pycello
import pycello.netlist
import pycello.target_data
import json
import unittest
import pickle

__author__ = 'Timothy S. Jones <jonests@bu.edu>, Densmore Lab, BU'
__license__ = 'GPL3'


class TestNetlist(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestNetlist, self).__init__(*args, **kwargs)

    @classmethod
    def setUpClass(cls):
        path = "examples/Cello-UCF/files/v2/ucf/Eco/Eco1C1G1T1.UCF.json"
        with open(path) as ucf_file:
            ucf = json.load(ucf_file)
        cls.ucf = pycello.target_data.TargetDataFile(ucf)
        path = "examples/and_outputNetlist.json"
        with open(path) as netlist_file:
            cls.netlist_json = json.load(netlist_file)
        # cls.maxDiff = 4000

    def test_netlist(self):
        pycello.netlist.Netlist(self.netlist_json)

    def test_netlist_node_json(self):
        netlist = pycello.netlist.Netlist(self.netlist_json)
        node = netlist.nodes[0]
        encoder = pycello.netlist.NodeEncoder
        dump = json.dumps(node, cls=encoder, indent=4)
        reference = '''{\n    "name": "a",\n    "nodeType": "PRIMARY_INPUT",\n    "partitionID": -1,\n    "deviceName": "LacI_sensor"\n}'''
        self.assertEqual(dump, reference)

        # netlist = pycello.netlist.Netlist(self.netlist, self.ucf)
        # nodes = set([node.name for node in netlist.nodes])
        # nodes_ref = set(['a', 'b', 'out', '$48', '$49', '$50'])

        # self.assertEqual(nodes, nodes_ref, "Incorrect node list.")

    # def test_ucf_netlist(self):
    #     with open('examples/and_outputNetlist.json') as netlist_file:
    #         netlist_json = json.load(netlist_file)

    #     netlist = pycello.netlist.Netlist(netlist_json, self.ucf)

    #     nodes = set([node.name for node in netlist.nodes])
    #     nodes_ref = set(['a', 'b', 'out', '$48', '$49', '$50'])

    #     self.assertEqual(nodes, nodes_ref, "Incorrect node list.")

    # def test_ucf_logiccircuit(self):
    #     with open('examples/0x78_A000_logic_circuit.txt') as lc_file:
    #         lc_text = lc_file.readlines()

    #     netlist = pycello.netlist.Netlist.fromLogicCircuit(lc_text, self.ucf)

    #     nodes = set([node.name for node in netlist.nodes])

    #     self.assertTrue("E1_BetI" in nodes, "Incorrect nodes.")

    # def test_json(self):
    #     with open('examples/0x78_Netlist.pickle', 'rb') as pickle_file:
    #         netlist = pickle.load(pickle_file)

    #     with open('examples/0x78_Netlist.json', 'r') as netlist_file:
    #         netlist_ref = netlist_file.read()

    #     netlist = json.dumps(netlist.json, indent=4)

    #     self.assertEqual(netlist, netlist_ref, "Incorrect node list.")


if __name__ == '__main__':
    unittest.main()
