"""

"""
import json
import logging
import numpy as np
from tarfile import ReadError
from typing import Dict, List, Optional, Union

import tvm
from tvm import rpc
from tvm.contrib import graph_executor as runtime
from tvm.relay.param_dict import load_param_dict

from .main import register_parser
from .model import TVMCLIPackage, TVMCLIResult

from tvmcli import TVMCLIException

logger = logging.getLogger("TVMCLI")


@register_parser
def add_runner_parser(subparser):
    """

    """
    parser = subparser.add_parser("run", help="run a compiled model.")
    parser.set_defaults(func=drive_run)

    parser.add_argument(
        "--device",
        choices=["cpu", "cuda"],
        default="cpu",
        help="target device to run the compiled model. Defaults to \"cpu\"",
    )
    parser.add_argument(
        "--fill-mode",
        choices=["zeros", "ones", "random"],
        default="random",
        help="fill all input tensors with values. In case --inputs/-i is provided, "
             "they will take precedence over --fill-mode. Any remaining inputs will be "
             "filled using the chosen fill mode. Defaults to \"random\"",
    )
    parser.add_argument("-i", "--inputs", metavar="", help="path to the .npz input file")
    parser.add_argument("-o", "--outputs", metavar="", help="path to the .npz output file")
    parser.add_argument(
        "--print-time", action="store_true", help="record and print the execution time(s)"
    )
    parser.add_argument(
        "--repeat", metavar="", type=int, default=1, help="run the model n times. Defaults to 1"
    )
    parser.add_argument(
        "--number", metavar="", type=int, default=1, help="repeat the run n times. Defaults to 1"
    )
    parser.add_argument(
        "--min-repeat-ms",
        metavar="",
        default=None,
        type=int,
        help="minimum time to run each trial, in milliseconds. "
             "Defaults to 0 on x86 and 1000 on all other targets",
    )
    parser.add_argument("FILE", help="path to the compiled module file")


def drive_run(args):
    """
    Invoke runner module with command line arguments

    Parameters
    ----------
    args: argparse.Namespace
        Arguments from command line parser.
    """
    try:
        inputs = np.load(args.inputs) if args.inputs else {}
    except IOError as ex:
        raise TVMCLIException("Error occurred during loading inputs file: %s", ex)

    try:
        tvmcli_package = TVMCLIPackage(package_path=args.FILE)
    except IsADirectoryError:
        raise TVMCLIException(f"File {args.FILE} must be an archive, not a directory.")
    except FileNotFoundError:
        raise TVMCLIException(f"File {args.FILE} does not exist.")
    except ReadError:
        raise TVMCLIException(f"Could not read model from archive {args.FILE}!")

    result = run_module(
        tvmcli_package,
        args.device,
        inputs=inputs,
        fill_mode=args.fill_mode,
        repeat=args.repeat,
        number=args.number,
        min_repeat_ms=args.min_repeat_ms
    )

    if args.print_time:
        stat_table = result.get_times()
        # print here is intentional
        print(stat_table)

    if args.outputs:
        # Save the outputs
        result.save(args.outputs)


def run_module(
        tvmcli_package: TVMCLIPackage,
        device: str,
        inputs: Optional[Dict[str, np.ndarray]] = None,
        fill_mode: str = "random",
        repeat: int = 10,
        number: int = 10,
        min_repeat_ms: Optional[int] = None,
):
    """

    Parameters
    ----------
    tvmcli_package
    device
    inputs
    fill_mode
    repeat
    number
    min_repeat_ms

    Returns
    -------

    """
    if not isinstance(tvmcli_package, TVMCLIPackage):
        raise TVMCLIException(
            "This model doesn't seem to have been compiled yet."
            "Try using tvmcli.compile or subparser 'compile' in CLI to compile the model before running it"
        )

    session = rpc.LocalSession()

    session.upload(tvmcli_package.lib_path)
    lib = session.load_module(tvmcli_package.lib_name)

    logger.info("Using device: %s.", device)
    if device == "cuda":
        dev = session.cuda()
    else:
        assert device == "cpu"
        dev = session.cpu()

    if min_repeat_ms is None:
        min_repeat_ms = 0 if device == "cpu" else 1000
        logging.info("Default --min-repeat-ms for input device is %s", min_repeat_ms)

    module = runtime.create(tvmcli_package.graph, lib, dev)

    logging.debug("Loading params into the runtime module.")
    module.load_params(tvmcli_package.params)

    shape_dict, type_dict = get_input_info(tvmcli_package.graph, tvmcli_package.params)
    input_dict = make_input_dict(shape_dict, type_dict, inputs, fill_mode)

    logger.debug("Setting inputs to the module")
    module.set_input(**input_dict)

    times = module.benchmark(dev, number=number, repeat=repeat)

    logger.debug("Collecting the outputs")
    num_outputs = module.get_num_outputs()
    outputs = {}
    for i in range(num_outputs):
        output_name = "output_{}".format(i)
        outputs[output_name] = module.get_output(i).numpy()

    return TVMCLIResult(outputs, times)


def generate_tensor_data(shape: tuple, dtype: str, fill_mode: str):
    """Generate data to produce a tensor of given shape and dtype.

    Random data generation depends on the dtype. For int8 types,
    random integers in the range 0->255 are generated. For all other
    types, random floats are generated in the range -1->1 and then
    cast to the appropriate dtype.

    This is used to quickly generate some data to input the models, as
    a way to check that compiled module is sane for running.

    Parameters
    ----------
    shape : tuple
        The shape of the tensor.
    dtype : str
        The dtype of the tensor.
    fill_mode : str
        The fill-mode to use, either "zeros", "ones" or "random".

    Returns
    -------
    tensor : np.array
        The generated tensor as a np.array.
    """
    if fill_mode == "zeros":
        tensor = np.zeros(shape=shape, dtype=dtype)
    elif fill_mode == "ones":
        tensor = np.ones(shape=shape, dtype=dtype)
    elif fill_mode == "random":
        if "int8" in dtype:
            tensor = np.random.randint(128, size=shape, dtype=dtype)
        else:
            tensor = np.random.uniform(-1, 1, size=shape).astype(dtype)
    else:
        raise TVMCLIException("unknown fill-mode: {}".format(fill_mode))

    return tensor


def get_input_info(graph_json_str: str, params: Dict[str, tvm.nd.NDArray]):
    """

    Parameters
    ----------
    graph_json_str
    params

    Returns
    -------

    """
    shape_dict = {}
    type_dict = {}
    params_dict = load_param_dict(params)
    param_names = [k for (k, v) in params_dict.items()]
    graph = json.loads(graph_json_str)

    for node_id in graph["arg_nodes"]:
        node = graph["nodes"][node_id]
        name = node["name"]
        if name not in param_names:
            shape_dict[name] = graph["attrs"]["shape"][1][node_id]
            type_dict[name] = graph["attrs"]["dltype"][1][node_id]

    logger.debug("Collecting graph input shape and type:")
    logger.debug("Graph input shape: %s", shape_dict)
    logger.debug("Graph input type: %s", type_dict)

    return shape_dict, type_dict


def make_input_dict(
        shape_dict: Dict[str, List[int]],
        type_dict: Dict[str, str],
        inputs: Optional[Dict[str, np.ndarray]] = None,
        fill_mode: str = "random",
):
    """

    Parameters
    ----------
    shape_dict
    type_dict
    inputs
    fill_mode

    Returns
    -------

    """
    logger.debug("making inputs dict")

    if inputs is None:
        inputs = {}

    for input_name in inputs:
        if input_name not in shape_dict.keys():
            raise TVMCLIException(
                "the input tensor '{}' is not in the graph. Expected inputs: '{}'".format(
                    input_name, shape_dict.keys()
                )
            )

    inputs_dict = {}
    for input_name in shape_dict:
        if input_name in inputs.keys():
            logger.debug("setting input '%s' using user's input data", input_name)
            inputs_dict[input_name] = inputs[input_name]
        else:
            shape = shape_dict[input_name]
            dtype = type_dict[input_name]

            logger.debug(
                "generating data for input '%s' (shape: %s, dtype: %s), using fill-mode: '%s'",
                input_name,
                shape,
                dtype,
                fill_mode
            )
            data = generate_tensor_data(shape, dtype, fill_mode)
            inputs_dict[input_name] = data

    return inputs_dict
