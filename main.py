import getopt
import sys

from cvalue import CValue


def c_value():
    """
    C-Value Method CLI Entrance
    :return: None
    """
    input_path = None
    output_path = None
    argv = sys.argv[1:]
    if not argv:
        raise ValueError
    opts, args = getopt.getopt(argv, "i:o:", ["input=", "output="])
    for opt, arg in opts:
        if opt in ["-i", "--input"]:
            input_path = arg
        if opt in ["-o", "--output"]:
            output_path = arg
    if not input_path or not output_path:
        raise ValueError
    CValue(input_path, output_path)


c_value()
