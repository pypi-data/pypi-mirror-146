"""

"""

import os
import tarfile
import json
from typing import Optional, Union, Dict, Callable, TextIO
import numpy as np

import tvm
from tvm import relay
from tvm.contrib import utils
from tvm.relay.backend.executor_factory import GraphExecutorFactoryModule
from tvm.runtime.module import BenchmarkResult

from tvmcli import TVMCLIException


class TVMCLIModel(object):
    """
    Initialize a TVMCLI Model from a model's relay representation or a previously saved TVMCLIModel

    Parameters
    ----------
    """

    def __init__(self,
                 mod: Optional[tvm.IRModule] = None,
                 params: Optional[Dict[str, tvm.nd.NDArray]] = None,
                 model_path: Optional[str] = None
                 ):
        self.lib_path = None
        if (mod is None or params is None) and (model_path is None):
            raise TVMCLIException("Either 'mod' and 'params' must be provided"
                                  "or a path to  a previously saved TVMCLIModel")
        self._tmp_dir = utils.tempdir()
        if model_path is not None:
            self.load(model_path)
        else:
            self.mod = mod
            self.params = params if params else {}

    def save(self, model_path: str):
        """
        Save the TVMCLIModel to disk

        This function only saves the model's relay graph representation,
        the parameters, and the tuning records if applicable.
        It won't save any compiled artifacts.

        Parameters
        ----------
        model_path

        Returns
        -------

        """
        temp = self._tmp_dir

        # Save relay graph
        relay_name = "model.json"
        relay_path = temp.relpath(relay_name)
        with open(relay_path, "w") as relay_file:
            relay_file.write(tvm.ir.save_json(self.mod))

        # Save params
        params_name = "model.params"
        params_path = temp.relpath(params_name)
        with open(params_path, "w") as params_file:
            params_file.write(relay.save_param_dict(self.params))

        # Create a tar file
        with tarfile.open(model_path, "w") as tar:
            tar.add(relay_path, relay_name)
            tar.add(params_path, params_name)

            if os.path.exists(self.default_tuning_records_path()):
                tar.add(self.default_tuning_records_path(), "tuning_records")

            if os.path.exists(self.default_package_path()):
                tar.add(self.default_package_path(), "model_package.tar")

    def load(self, model_path: str):
        """
        Load a previously saved TVMCLIModel from disk

        Parameters
        ----------
        model_path

        Returns
        -------

        """

        # Extract content from saved tar file
        temp = self._tmp_dir
        t = tarfile.open(model_path)
        t.extractall(temp.relpath("."))

        # Load model's relay graph
        relay_path = temp.relpath("model.json")
        with open(relay_path, "r") as relay_file:
            self.mod = tvm.ir.load_json(relay_file.read())

        # Load model's parameters
        relay_params = temp.relpath("model.params")
        with open(relay_params, "r") as params_file:
            self.params = relay.load_param_dict(params_file.read())

    def default_tuning_records_path(self):
        """

        Returns
        -------

        """
        return self._tmp_dir.relpath("tuning_records")

    def default_package_path(self):
        """

        Returns
        -------

        """
        return self._tmp_dir.relpath("model_package.tar")

    def export_package(self,
                       executor_factory: GraphExecutorFactoryModule,
                       package_path: Optional[str] = None,
                       output_format: str = "so"
                       ):
        """
        Save TVMCLIModel to a specific path.

        Parameters
        ----------
        executor_factory
        package_path
        output_format

        Returns
        -------

        """

        lib_name = "mod." + output_format
        graph_name = "mod.json"
        param_name = "mod.params"

        temp = self._tmp_dir
        if package_path is None:
            package_path = self.default_package_path()
        path_lib = temp.relpath(lib_name)

        executor_factory.get_lib().export_library(path_lib)

        with open(temp.relpath(graph_name), "w") as graph_file:
            graph_file.write(executor_factory.get_graph_json())

        with open(temp.relpath(param_name), "wb") as param_file:
            param_file.write(relay.save_param_dict(executor_factory.get_params()))

        with tarfile.open(package_path, "w") as tar:
            tar.add(path_lib, lib_name)
            tar.add(temp.relpath(graph_name), graph_name)
            tar.add(temp.relpath(param_name), param_name)

        return package_path

    def summary(self, file: TextIO = None):
        """Print the relay IR corressponding to this model.

        Arguments
        ---------
        file: Writable, optional
            If specified, the summary will be written to this file.
        """
        print(self.mod, file=file)


class TVMCLIPackage(object):
    """
    Load a saved TVMCLIPackage from disk

    """

    def __init__(self, package_path: str):
        self.graph = None
        self.params = None
        self.lib_name = None
        self.lib_path = None
        self._tmp_dir = utils.tempdir()
        self.package_path = package_path
        self.import_package(package_path)

    def import_package(self, package_path: str):
        """
        Load a TVMCLIPackage from a previously exported TVMCLIModel.

        Parameters
        ----------
        package_path

        """
        temp = self._tmp_dir
        t = tarfile.open(package_path)
        t.extractall(temp.relpath("."))

        libname_so = "mod.so"
        libname_tar = "mod.tar"

        if os.path.exists(temp.relpath(libname_so)):
            self.lib_name = libname_so
        elif os.path.exists(temp.relpath(libname_tar)):
            self.lib_name = libname_tar
        else:
            raise TVMCLIException("Could not find exported library in the package.")
        self.lib_path = temp.relpath(self.lib_name)

        graph = temp.relpath("mod.json")
        params = temp.relpath("mod.params")

        with open(params, "rb") as param_file:
            self.params = bytearray(param_file.read())

        if graph is not None:
            with open(graph) as graph_file:
                self.graph = graph_file.read()
        else:
            self.graph = None


class TVMCLIResult(object):
    """

    """

    def __init__(self,
                 outputs: Dict[str, np.ndarray],
                 times: BenchmarkResult
                 ):
        """


        Parameters
        ----------
        outputs
        times
        """
        self.outputs = outputs
        self.times = times

    def get_times(self):
        """

        Returns
        -------

        """
        return str(self.times)

    def get_output(self, name: str):
        """


        Parameters
        ----------
        name

        Returns
        -------

        """
        return self.outputs[str]

    def save(self, output_path: str):
        """


        Parameters
        ----------
        output_path

        Returns
        -------

        """
        np.savez(output_path, **self.outputs)

    def __str__(self):
        stat_table = self.get_times()
        output_keys = f"Output Names:\n {list(self.outputs.keys())}"
        return stat_table + "\n" + output_keys
