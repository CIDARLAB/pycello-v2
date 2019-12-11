import pycello2.netlist
import pycello2.ucf
import json
import unittest

__author__ = 'Timothy S. Jones <jonests@bu.edu>, Densmore Lab, BU'
__license__ = 'GPL3'


class TestNetlist(unittest.TestCase):

    def test_ucf_netlist(self):
        with open('../examples/Eco1C1G1T1-synbiohub.UCF.json') as ucf_file:
            ucf_json = json.load(ucf_file)

        with open('../examples/and_outputNetlist.json') as netlist_file:
            netlist_json = json.load(netlist_file)

        ucf = pycello2.ucf.UCF(ucf_json)
        netlist = pycello2.netlist.Netlist(netlist_json, ucf)

        nodes = set([node.name for node in netlist.nodes])
        nodes_literal = set(['a', 'b', 'out', '$48', '$49', '$50'])

        self.assertEqual(nodes, nodes_literal, "Incorrect node list.")


if __name__ == '__main__':
    unittest.main()
