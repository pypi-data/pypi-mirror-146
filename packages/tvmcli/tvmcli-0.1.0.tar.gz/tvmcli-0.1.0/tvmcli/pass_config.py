"""
TVMCLI PassContext Interface
"""

import importlib

import tvm
from tvmcli import TVMCLIException


def get_pass_config_value(name, value, config_type):
    """

    Parameters
    ----------
    name
    value
    config_type

    Returns
    -------

    """
    if config_type == "IntImm":
        mapping_values = {
            "false": False,
            "true": True,
        }

        if value.isdigit():
            parsed_value = int(value)
        else:
            parsed_value = mapping_values.get(value.lower(), None)

        if parsed_value is None:
            raise TVMCLIException(f"Invalid value '{value}' for configuration '{name}'.")

    if config_type == "runtime.String":
        parsed_value = value

    return parsed_value


def parse_configs(input_configs):
    """
    Parse compile configuration values set via CLI.

    Parameters
    ----------
    input_configs

    Returns
    -------

    """
    if not input_configs:
        return {}

    all_configs = tvm.ir.transform.PassContext.list_configs()
    supported_config_types = ("IntImm", "runtime.String")
    supported_configs = [
        config for config in all_configs.keys() if all_configs[config]["type"] in supported_config_types
    ]

    pass_context_configs = {}

    for config in input_configs:
        if not config:
            raise TVMCLIException(
                f"Invalid format for configuration '{config}', use <config>=<value>"
            )

        # Each config is expected to be provided as "name=value"
        try:
            name, value = config.split("=")
            name = name.strip()
            value = value.strip()
        except ValueError:
            raise TVMCLIException(
                f"Invalid format for configuration '{config}', use <config>=<value>"
            )

        if name not in all_configs:
            raise TVMCLIException(
                f"Configuration '{name}' is not defined in TVM. "
                f"These are the existing configurations: {', '.join(all_configs)}"
            )

        if name not in supported_configs:
            raise TVMCLIException(
                f"Configuration '{name}' uses a data type not supported by TVMCLI. "
                f"The following configurations are supported: {', '.join(supported_configs)}"
            )

        parsed_value = get_pass_config_value(name, value, all_configs[name]["type"])
        pass_context_configs[name] = parsed_value

    return pass_context_configs
