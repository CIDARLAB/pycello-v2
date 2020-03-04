from .context import pycello
import pycello.target_data
import json
import unittest

__author__ = 'Timothy S. Jones <jonests@bu.edu>, Densmore Lab, BU'
__license__ = 'GPL3'


class TestUserConstraintsFile(unittest.TestCase):

    def test_user_constraints_file(self):
        with open('examples/Cello-UCF/files/v2/ucf/Eco/Eco1C1G1T1.UCF.json') as ucf_file:
            ucf = json.load(ucf_file)
        ucf = pycello.target_data.UserConstraintsFile(ucf)


if __name__ == '__main__':
    unittest.main()
