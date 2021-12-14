import getopt
import sys

from segment import Segment


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


class CValue(object):

    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.corpus = None
        self.output_file = output_file

    def terms_extraction(self):
        candidate_terms = Segment.segment(self.corpus)
        return

    def core_algorithm(self):
        return

    def terms_export(self):
        pass


c_value()
