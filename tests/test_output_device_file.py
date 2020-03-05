import unittest
from glob import glob
from os.path import basename
from .context import pycello
import pycello.target_data
from .meta_test import TestFileMeta, get_json_file_contents

__author__ = 'Timothy S. Jones <jonests@bu.edu>, Densmore Lab, BU'
__license__ = 'GPL3'


class TestOutputDeviceFile(unittest.TestCase, metaclass=TestFileMeta):

    def get_test_args():
        pattern = "examples/Cello-UCF/files/v2/output/**/*.output.json"
        files = glob(pattern, recursive=True)
        for f in files:
            yield (basename(f), f)

    def _test_output_device_file(self, f):
        odf = get_json_file_contents(f)
        pycello.target_data.TargetDataFile(odf)


if __name__ == '__main__':
    unittest.main()
