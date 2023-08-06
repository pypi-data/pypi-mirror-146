""" Define and retrieve all command line options.
"""

import argparse


def get_command_line_arguments(version: str):
    """build, parse and return command line arguments

    Args:
        version (str): the current program version

    Returns:
        the parsed command line arguments
    """

    program_name = "mrcsmooth"
    description = ("Uses a filter on a three dimensional density data "
                   "to reduce the number of voxels by 2 for each pass, "
                   "effectively smoothening the data while reducing "
                   "the data size.")

    parser = argparse.ArgumentParser(
        description=description,
        prog=program_name,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--density",
                        required=True,
                        help="input mrc density filename",
                        metavar="input.mrc")

    parser.add_argument("--output-density",
                        nargs='?',
                        default='smooth.mrc',
                        help="file to write the fitted structure to.",
                        metavar="smooth.mrc")

    parser.add_argument("--passes",
                        type=int,
                        default=1,
                        help="how often to apply the filter, "
                             "however have at least 4 voxels "
                             "per dimension in the output data.")

    parser.add_argument("--version",
                        action="version",
                        version=(f"{program_name} {version}"))

    return parser.parse_args()
