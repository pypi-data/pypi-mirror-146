"""
Provides support to auto-tuning networks using Auto-Scheduler a.k.a Ansor
"""
import os.path
import logging
from typing import Any, Optional, Dict, List, Union

import tvm
from tvm import auto_scheduler

from . import frontends
from .main import register_parser
from .shape_parser import parse_shape_string
from .target import generate_target_args, reconstruct_target_args, target_from_cli
from .model import TVMCLIModel

logger = logging.getLogger('TVMCLI')


@register_parser
def add_tune_parser(subparsers):
    """Include parser for 'tune' subcommand"""

    parser = subparsers.add_parser("tune", help="auto-tune a model using auto-scheduler")
    parser.set_defaults(func=drive_tune)

    # There is some extra processing required to define the actual default value
    # for --min-repeat-ms. This is done in `tune_model`.
    parser.add_argument("FILE", help="path to the input model file")
    parser.add_argument(
        "-o",
        "--output",
        metavar="",
        default="tuning_records.json",
        help="output file to store the tuning records for the tuning process, default to \"tuning_records.json\"",
    )

    parser.add_argument(
        "-f",
        "--model-format",
        choices=frontends.get_frontend_names(),
        help="specify input model's format",
    )
    parser.add_argument(
        "--input-shapes",
        metavar="",
        help="specify non-generic shapes for model to run, format is "
             '"input_name:[dim1,dim2,...,dimn] input_name2:[dim1,dim2]"',
        type=parse_shape_string,
    )

    auto_scheduler_measurement_group = parser.add_argument_group(
        "Measurement options",
    )
    auto_scheduler_measurement_group.add_argument(
        "--number",
        metavar="",
        default=10,
        type=int,
        help="number of runs a single repeat is made of. "
             "The final number of tuning executions is: "
             "(1 + number * repeat)",
    )
    auto_scheduler_measurement_group.add_argument(
        "--timeout",
        metavar="",
        type=int,
        default=10,
        help="compilation timeout, in seconds"
    )
    auto_scheduler_measurement_group.add_argument(
        "--repeat",
        metavar="",
        type=int,
        default=1,
        help="how many times to repeat each measurement",
    )
    auto_scheduler_measurement_group.add_argument(
        "--min-repeat-ms",
        metavar="",
        default=None,
        type=int,
        help="minimum time to run each trial, in milliseconds. "
             "Defaults to 0 on x86 and 1000 on all other targets",
    )

    auto_scheduler_tune_group = parser.add_argument_group(
        "Tune options",
    )
    auto_scheduler_tune_group.add_argument(
        "--include-simple-tasks",
        help="whether to extract simple tasks that do not include complicated ops",
        action="store_true",
    )
    auto_scheduler_tune_group.add_argument(
        "--log-estimated-latency",
        help="whether to log the estimated latency to the file after tuning a task",
        action="store_true",
    )
    auto_scheduler_tune_group.add_argument(
        "--early-stopping",
        metavar="",
        type=int,
        help="minimum number of trials before early stopping",
    )
    auto_scheduler_tune_group.add_argument(
        "--trials",
        metavar="",
        type=int,
        default=1000,
        help="the maximum number of tuning trials to perform",
    )
    auto_scheduler_tune_group.add_argument(
        "--tuning-records",
        metavar="",
        help="path to an auto-tuning log file by Auto-Scheduler, which will be "
             "continued in this tuning process",
    )

    parser.add_argument(
        "--target",
        default="llvm",
        metavar="",
        help="compilation target as plain string, "
             "e.g. \"llvm -keys=cpu -mcpu=<mycpu> -mtriple=<mytriple> -mattr='+<feature1>, -<feature2>'\", "
             "default to \"llvm\""
    )
    # generate_target_args(parser)


def drive_tune(args):
    """
    Invoke auto-tuning process using command line's arguments


    Parameters
    ----------
    args: argparse.Namespace
        Arguments from command line parser.
    """
    model = frontends.load_model(args.FILE, args.model_format, shape_dict=args.input_shapes)

    tune_model(
        model,
        args.target,
        tuning_records=args.output,
        prior_records=args.tuning_records,
        trials=args.trials,
        min_repeat_ms=args.min_repeat_ms,
        early_stopping=args.early_stopping,
        timeout=args.timeout,
        repeat=args.repeat,
        number=args.number,
        include_simple_tasks=args.include_simple_tasks,
        log_estimated_latency=args.log_estimated_latency,
        additional_target_options=None,
        # additional_target_options=reconstruct_target_args(args),
    )


def tune_model(
        tvmcli_model: TVMCLIModel,
        target: str,
        tuning_records: Optional[str] = None,
        prior_records: Optional[str] = None,
        trials: int = 1000,
        min_repeat_ms: Optional[int] = None,
        early_stopping: Optional[int] = None,
        timeout: int = 10,
        repeat: int = 1,
        number: int = 10,
        include_simple_tasks: bool = False,
        log_estimated_latency: bool = False,
        additional_target_options: Optional[Dict[str, Dict[str, Any]]] = None,
):
    """

    Parameters
    ----------
    tvmcli_model
    target
    tuning_records
    prior_records
    trials
    min_repeat_ms
    early_stopping
    timeout
    repeat
    number
    include_simple_tasks
    log_estimated_latency
    additional_target_options

    Returns
    -------

    """
    target = target_from_cli(target, additional_target_options)

    mod = tvmcli_model.mod
    params = tvmcli_model.params

    if tuning_records is None:
        tuning_records = tvmcli_model.default_tuning_records_path()

    if min_repeat_ms is None:
        min_repeat_ms = 0 if target.keys[0] == "cpu" else 1000
        logging.info("Default --min-repeat-ms for input target is %s", min_repeat_ms)

    runner_ctx = auto_scheduler.LocalRPCMeasureContext(
        number=number,
        timeout=timeout,
        repeat=repeat,
        min_repeat_ms=min_repeat_ms
    )

    tasks, weights = auto_scheduler.extract_tasks(
        mod["main"],
        params,
        target=target,
        include_simple_tasks=include_simple_tasks
    )

    tuning_options = auto_scheduler.TuningOptions(
        num_measure_trials=trials,
        measure_callbacks=[auto_scheduler.RecordToFile(tuning_records)],
        runner=runner_ctx.runner,
        early_stopping=early_stopping
    )

    logging.info("Do auto-tuning process by Auto-Scheduler using options: %s", tuning_options)

    if not log_estimated_latency:
        callbacks = [auto_scheduler.task_scheduler.PrintTableInfo()]
    else:
        callbacks = [
            auto_scheduler.task_scheduler.PrintTableInfo(),
            auto_scheduler.task_scheduler.LogEstimatedLatency(("total_latency.tsv")),
        ]

    tuner = auto_scheduler.TaskScheduler(
        tasks, weights, load_model_file=prior_records, callbacks=callbacks
    )

    tuner.tune(tuning_options)
