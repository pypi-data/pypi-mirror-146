"""

"""
import json
import logging
import os.path
import re

import tvm
from tvm.target.target import Target

from tvmcli import TVMCLIException

logger = logging.getLogger("TVMCLI")

SUPPORTED_TARGETS = [
    "llvm",
    "cuda"
]

# We can't tell the type inside an Array but all current options are strings so
# it can default to that. Bool is used alongside Integer but aren't distinguished
# between as both are represented by IntImm
INTERNAL_TO_NATIVE_TYPE = {"runtime.String": str, "IntImm": int, "Array": str}
INTERNAL_TO_HELP = {"runtime.String": " string", "IntImm": " int/bool", "Array": " options"}


def generate_target_args(parser):
    """Walks through the TargetKind registry and generates arguments for each Target's options"""
    for target_kind in _valid_target_kinds():
        target = Target(target_kind)
        _generate_target_kind_args(parser, target.kind)


def _valid_target_kinds():
    """
    Return all supported targets.
    """
    return SUPPORTED_TARGETS

def _generate_target_kind_args(parser, kind):
    target_group = parser.add_argument_group(f"target {kind.name}")
    for target_option, target_type in kind.options.items():
        if target_type in INTERNAL_TO_NATIVE_TYPE:
            target_group.add_argument(
                f"--target-{kind.name}-{target_option}",
                type=INTERNAL_TO_NATIVE_TYPE[target_type],
                help=f"target {kind.name} {target_option}{INTERNAL_TO_HELP[target_type]}",
            )


def _recombine_target(target):
    name = target["name"]
    opts = " ".join([f"-{key}={value}" for key, value in target["opts"].items()])
    return f"{name} {opts}"


def _combine_target_options(target, additional_target_options=None):
    if additional_target_options is None:
        return target
    if target["name"] in additional_target_options:
        target["opt"].update(additional_target_options[target["name"]])
    return target


def _reconstruct_target_kind_args(args, kind):
    kind_options = {}
    for target_option, target_type in kind.options.items():
        if target_type in INTERNAL_TO_NATIVE_TYPE:
            var_name = f"target_{kind.name.replace('-', '_')}_{target_option.replace('-', '_')}"
            option_value = getattr(args, var_name)
            if option_value is not None:
                kind_options[target_option] = getattr(args, var_name)
    return kind_options


def tokenize_target(target):
    """

    Parameters
    ----------
    target

    Returns
    -------

    """
    target_pattern = (
        r"(\-{0,2}[\w\-]+\=?"
        r"(?:[\w\+\-\.]+(?:,[\w\+\-\.])*"
        r"|[\'][\w\+\-,\s\.]+[\']"
        r"|[\"][\w\+\-,\s\.]+[\"])*"
        r"|,)"
    )

    return re.findall(target_pattern, target)


def parse_target(target):
    """

    Parameters
    ----------
    target

    Returns
    -------

    """
    codegens = []
    tvm_target_kinds = _valid_target_kinds()
    parsed_tokens = tokenize_target(target)

    split_codegens = []
    current_codegen = []
    split_codegens.append(current_codegen)
    for token in parsed_tokens:
        if token == ",":
            current_codegen = []
            split_codegens.append(current_codegen)
        else:
            current_codegen.append(token)

    for codegen_def in split_codegens:
        name = codegen_def[0]
        is_supported_target = name in SUPPORTED_TARGETS
        raw_target = " ".join(codegen_def)
        all_opts = codegen_def[1:] if len(codegen_def) > 1 else []
        opts = {}
        for opt in all_opts:
            try:
                if opt.startswith("--"):
                    opt_name = opt[2:]
                    opt_value = True
                else:
                    opt = opt[1:] if opt.startswith("-") else opt
                    opt_name, opt_value = opt.split("=", maxsplit=1)

                    opt_value = opt_value[1:-1] if opt_value[0] in ('"', "'") else opt_value
            except ValueError:
                raise ValueError(f"Error occurred when parsing '{opt}'")

            opts[opt_name] = opt_value

        codegens.append(
            {"name": name, "opts": opts, "raw": raw_target, "is_supported_target": is_supported_target}
        )

    return codegens


def target_from_cli(target, additional_target_options=None):
    """


    Parameters
    ----------
    target
    additional_target_options

    Returns
    -------

    """
    if os.path.isfile(target):
        with open(target) as target_file:
            logger.debug("target input is a path: %s", target)
            target = "".join(target_file.readline())
    elif is_inline_json(target):
        logger.debug("target input is inline JSON: %s", target)
    else:
        logger.debug("target input is plain text: %s", target)
        try:
            parsed_target = parse_target(target)
        except ValueError as e:
            raise TVMCLIException(f"Error occurred during parsing target string '{target}'.\nThe error is: {e}")

        validate_targets(parsed_target, additional_target_options)
        tvm_targets = [
            _combine_target_options(t, additional_target_options)
            for t in parsed_target
            if t["is_supported_target"]
        ]

        target = _recombine_target(tvm_targets[-1])

    return Target(target, host=None)


def validate_targets(parse_targets, additional_target_options=None):
    """


    Parameters
    ----------
    parse_targets
    additional_target_options

    Returns
    -------

    """
    # tvm_target_kinds = tvm.target.Target.list_kinds()
    targets = [t["name"] for t in parse_targets]

    if len(targets) > len(set(targets)):
        raise TVMCLIException("Duplicate target definitions are not allowed")

    if targets[-1] not in SUPPORTED_TARGETS:
        supported_targets = ", ".join(SUPPORTED_TARGETS)
        raise TVMCLIException(
            f"The last target needs to be a supported TVM target. currently supported choices: {supported_targets}"
        )

    tvm_targets = [t for t in targets if t in SUPPORTED_TARGETS]
    if len(tvm_targets) > 1:
        verbose_tvm_targets = ", ".join(tvm_targets)
        logger.info(f"Found more than one supported targets: {verbose_tvm_targets}, use last one as default.")

    if additional_target_options is not None:
        for target_name in additional_target_options:
            if not any([target for target in parse_targets if target["name"] == target_name]):
                first_options = list(additional_target_options[target_name].kets())[0]
                raise TVMCLIException(
                    f"Passed --target-{target_name}-{first_options}"
                    f" but didn't specify {target_name} target"
                )


def reconstruct_target_args(args):
    """

    """
    reconstructed_target = {}
    for target_kind in _valid_target_kinds():
        target = Target(target_kind)
        kind_options = _reconstruct_target_kind_args(args, target.kind)
        if kind_options:
            reconstructed_target[target.kind.name] = kind_options

    return reconstructed_target


def is_inline_json(target):
    """
    Return whether the 'target' argument via CLI is a json file.

    Parameters
    ----------
    target

    Returns
    -------

    """
    try:
        json.loads(target)
        return True
    except json.decoder.JSONDecodeError:
        return False
