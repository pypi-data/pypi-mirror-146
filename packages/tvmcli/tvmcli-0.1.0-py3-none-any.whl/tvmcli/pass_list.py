"""
TVMCLI Pass List Management
"""

import argparse

import tvm
from tvm._ffi import registry


def parse_pass_list_str(input_string):
    """Parse an input string for existing passes

    Parameters
    ----------
    input_string: str
        Possibly comma-separated string with the names of passes

    Returns
    -------
    list: a list of existing passes.
    """
    _prefix = "relay._transform."
    pass_list = input_string.split(",")
    missing_list = [
        p.strip()
        for p in pass_list
        if len(p.strip()) > 0 and tvm.get_global_func(_prefix + p.strip(), True) is None
    ]
    if len(missing_list) > 0:
        available_list = [
            n[len(_prefix) :] for n in registry.list_global_func_names() if n.startswith(_prefix)
        ]
        raise argparse.ArgumentTypeError(
            "Following passes are not registered within tvm: {}. Available: {}.".format(
                ", ".join(missing_list), ", ".join(sorted(available_list))
            )
        )
    return pass_list
