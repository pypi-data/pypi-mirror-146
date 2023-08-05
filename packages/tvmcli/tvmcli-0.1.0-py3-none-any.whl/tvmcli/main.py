"""
TVMCLI - A command-line interface for TVM
"""

import argparse
import logging
import sys

import tvm
from tvmcli import TVMCLIException

REGISTERED_PARSER = []


def register_parser(build_subparser):
    """

    Parameters
    ----------
    build_subparser

    Returns
    -------

    """
    REGISTERED_PARSER.append(build_subparser)
    return build_subparser


def _main(argv):
    """TVM command line interface main function"""
    parser = argparse.ArgumentParser(
        prog="tvmcli",
        description="tvmcli - a command line interface for TVM",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-v", "--verbose", action="count", default=0, help="increase log's verbosity.")
    parser.add_argument("--version", action="store_true", help="print TVM's version int current env and exit.")

    subparser = parser.add_subparsers(title="subcommands")
    for build_subparser in REGISTERED_PARSER:
        build_subparser(subparser)

    args = parser.parse_args(argv)
    if args.verbose > 4:
        args.verbose = 4

    logging.getLogger("TVMCLI").setLevel(40 - args.verbose * 10)

    if args.version:
        sys.stdout.write("%s\n" % tvm.__version__)
        return 0

    if not hasattr(args, "func"):
        parser.print_help(sys.stderr)
        return 1

    try:
        args.func(args)
    except TVMCLIException as err:
        sys.stderr.write("Error: %s\n" % err)
        return -1


def main():
    sys.exit(_main(sys.argv[1:]))


if __name__ == '__main__':
    main()
