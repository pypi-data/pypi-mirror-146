import logging
from abc import ABC
from abc import abstractmethod
from typing import Optional, List, Dict
from pathlib import Path

from tvmcli import TVMCLIException
from tvmcli.model import TVMCLIModel
from tvm import relay

logger = logging.getLogger("TVMCLI")


class Frontend(ABC):
    """Abstract class for command line driver frontend.

    Provide a unified way to import models (as files), and deal
    with any required preprocessing to create a TVM relay module from it."""

    @staticmethod
    @abstractmethod
    def name():
        """Frontend framework name"""

    @staticmethod
    @abstractmethod
    def suffixes():
        """File suffixes (extensions) used by this frontend framework"""

    @abstractmethod
    def load(self, path, shape_dict=None, **kwargs):
        """Load a model from a given path

        Parameters
        ----------
        path: str
            Path to the given model
        shape_dict: dict, optional
            Mapping from input names to their shapes

        Returns
        -------
        mod: tvm.IRModule
            The produced relay module
        params: dict
            The parameters (weights) for the relay module

        """


class OnnxFrontend(Frontend):
    """ONNX frontend framework for TVMCLI"""

    @staticmethod
    def name():
        return "onnx"

    @staticmethod
    def suffixes():
        return ["onnx"]

    def load(self, path, shape_dict=None, **kwargs):
        import onnx

        model = onnx.load(path)
        return relay.frontend.from_onnx(model, shape=shape_dict, **kwargs)


class TensorflowFrontend(Frontend):

    @staticmethod
    def name():
        return "pb"

    @staticmethod
    def suffixes():
        return ["pb"]

    def load(self, path, shape_dict=None, **kwargs):
        import tensorflow as tf
        import tvm.relay.testing.tf as tf_testing

        with tf.io.gfile.GFile(path, "rb") as tf_graph:
            content = tf_graph.read()

        graph_def = tf.compat.v1.GraphDef()
        graph_def.ParseFromString(content)
        graph_def = tf_testing.ProcessGraphDefParam(graph_def)

        logger.debug("parse Tensorflow model ans convert it into Relay computation graph")
        return relay.frontend.from_tensorflow(graph_def, shape=shape_dict, **kwargs)


class PytorchFrontend(Frontend):

    @staticmethod
    def name():
        return "pytorch"

    @staticmethod
    def suffixes():
        return ["pth", "zip"]

    def load(self, path, shape_dict=None, **kwargs):
        import torch

        if shape_dict is None:
            raise TVMCLIException("--input-shapes must be specified for %s" % self.name())

        traced_model = torch.jit.load(path)
        # switch to inference mode
        traced_model.eval()

        # convert shape dictionary to list for Pytorch frontend compatibility
        input_shapes = list(shape_dict.items())

        logger.debug("parse Torch model and convert it into Relay computation graph")
        return relay.frontend.from_pytorch(
            traced_model, input_shapes, keep_quantized_weight=True, **kwargs
        )


ALL_FRONTENDS = [
    OnnxFrontend,
    TensorflowFrontend,
    PytorchFrontend
]


def get_frontend_names():
    """
    Return the names of all supported frontend frameworks.

    Returns
    -------
    List: List of str
        A list of frontend framework names as strings

    """
    return [frontend.name() for frontend in ALL_FRONTENDS]


def get_frontend_by_name(name: str):
    """
    Try to get a frontend instance, based on the name provided.

    Parameters
    ----------
    name

    Returns
    -------

    """
    for frontend in ALL_FRONTENDS:
        if name == frontend.name():
            return frontend()

    raise TVMCLIException(
        "unrecognized frontend '{0}'. Please choose from supported frontends: {1}".fromat(name, get_frontend_names())
    )


def get_frontend_without_name(path: str):
    """
    This function will try to imply which frontend framework is being used,
    based on the extension of the file provided by the parameter 'path'.

    Parameters
    ----------
    path

    Returns
    -------

    """
    suffix = Path(path).suffix.lower()
    if suffix.startswith("."):
        suffix = suffix[1:]

    for frontend in ALL_FRONTENDS:
        if suffix in frontend.suffixes():
            return frontend()

    raise TVMCLIException("failed to infer the model's format. "
                          "Please specify it by using option '--model-format'")


def load_model(path: str,
               model_format: Optional[str] = None,
               shape_dict: Optional[Dict[str, List[int]]] = None,
               **kwargs
               ):
    """
    Load a model from a supported frontend framework and convert it into
    equivalent relay representation.

    Parameters
    ----------
    path
    model_format
    shape_dict
    kwargs

    Returns
    -------

    """

    if model_format is not None:
        frontend = get_frontend_by_name(model_format)
    else:
        frontend = get_frontend_without_name(path)

    mod, params = frontend.load(path, shape_dict, **kwargs)

    return TVMCLIModel(mod, params)
