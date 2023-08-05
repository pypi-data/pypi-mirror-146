import logging
import os.path
from typing import Any, Optional, Dict, List
from pathlib import Path

from . import frontends
from . import shape_parser, pass_list, pass_config
from .target import target_from_cli, reconstruct_target_args, generate_target_args
from .model import TVMCLIModel, TVMCLIPackage
from .main import register_parser

from tvmcli import TVMCLIException

import tvm
from tvm import auto_scheduler
from tvm import relay

logger = logging.getLogger('TVMCLI')


@register_parser
def build_compile_parser(subparsers):
    """

    """

    parser = subparsers.add_parser("compile", help="compile a model")
    parser.set_defaults(func=drive_compile)
    parser.add_argument(
        "-f",
        "--model-format",
        choices=frontends.get_frontend_names(),
        help="specify input model's format."
    )
    parser.add_argument(
        "-d",
        "--dump",
        action="store_true",
        help="dump model's relay representation code."
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="",
        default="module.tar",
        help="output the compiled module to a specified archive, which defaults to \"module.tar\""
    )
    parser.add_argument(
        "-O",
        "--opt-level",
        default=3,
        type=int,
        choices=range(0, 4),
        help="specify optimization level to use. Defaults to 3."
    )
    parser.add_argument(
        "FILE",
        help="path to the input model file."
    )
    parser.add_argument(
        "--tune-records",
        metavar="",
        default="",
        help="path to an auto-tuning log file created by AutoTVM or AutoScheduler during tuning. "
    )
    parser.add_argument(
        "--input-shapes",
        metavar="",
        help="specify input shapes for model to run, format is"
             '"input_name:[dim1,dim2,...,dimn] input_name2:[dim1,dim2,...]".',
        type=shape_parser.parse_shape_string,
        default=None
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="increase log's verbosity."
    )
    parser.add_argument(
        "--pass-config",
        action="append",
        metavar="",
        help="configurations to be used at compile time. "
             "This option can be provided multiple times, each time to set one configuration, "
             "e.g. \"--pass-config relay.backend.use_auto_scheduler=0\""
    )
    parser.add_argument(
        "--disabled-pass",
        metavar="",
        help="comma seperated list of compile passes going to be disabled.",
        type=pass_list.parse_pass_list_str,
        default=""
    )
    # generate_target_args(parser)
    parser.add_argument(
        "--target",
        default="llvm",
        metavar="",
        help="compilation target as plain string, "
             "e.g. \"llvm -keys=cpu -mcpu=<mycpu> -mtriple=<mytriple> -mattr='+<feature1>, -<feature2>'\", "
             "default to \"llvm\""
    )


def drive_compile(args):
    """
    Invoke tvmcli.compiler module with CLI arguments

    Parameters
    ----------
    args:argparse.Namespace
        Arguments from command line parser.
    """
    tvmcli_model = frontends.load_model(args.FILE, args.model_format, args.input_shapes)

    compile_model(tvmcli_model,
                  args.target,
                  tune_records=args.tune_records,
                  package_path=args.output,
                  disabled_pass=args.disabled_pass,
                  pass_context_config=args.pass_config,
                  dump_code=args.dump,
                  additional_target_options=None,
                  opt_level=args.opt_level
                  # additional_target_options=reconstruct_target_args(args)
                  )


def compile_model(tvmcli_model: TVMCLIModel,
                  target: str,
                  tune_records: Optional[str] = None,
                  package_path: Optional[str] = None,
                  dump_code: Optional[List[str]] = None,
                  opt_level: Optional[int] = 3,
                  disabled_pass: Optional[str] = None,
                  pass_context_config: Optional[List[str]] = None,
                  additional_target_options: Optional[Dict[str, Dict[str, Any]]] = None
                  ):
    """
    Compile a model from a supported frontend framework into a TVM module,
    which can be executed using the graph executor

    Parameters
    ----------
    tvmcli_model
    target
    tune_records
    package_path
    dump_code
    disabled_pass
    pass_context_config

    Returns
    -------

    """
    mod, params = tvmcli_model.mod, tvmcli_model.params

    config = pass_config.parse_configs(pass_context_config)

    tvm_target = target_from_cli(target, additional_target_options)

    if tune_records and os.path.exists(tune_records):
        logger.debug("tune records file provided: %s", tune_records)

        try:
            auto_scheduler.load_records(tune_records)
        except tvm._ffi.base.TVMError as e:
            raise TVMCLIException(f"load tune records failed with exception: {e}")

        with auto_scheduler.ApplyHistoryBest(tune_records):
            config["relay.backend.use_auto_scheduler"] = True
            with tvm.transform.PassContext(
                    opt_level=opt_level, config=config, disabled_pass=disabled_pass
            ):
                logger.debug("building relay graph with autoscheduler")
                graph_module = relay.build(mod, target=tvm_target, params=params)
    else:
        with tvm.transform.PassContext(opt_level=opt_level, config=config, disabled_pass=disabled_pass):
            logger.debug("building relay graph without tuning records")
            graph_module = relay.build(mod, target=tvm_target, params=params)

    package_path = tvmcli_model.export_package(graph_module, package_path)

    if dump_code:
        dump_file_name = package_path + '.relay'
        with open(Path(".", dump_file_name), "w") as dump_file:
            dump_file.write(str(mod))

    return TVMCLIPackage(package_path)
