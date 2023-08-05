"""
TVMCLI - A command-line interface for TVM
"""


class TVMCLIException(Exception):
    """TVMCLI Exception"""


class TVMCLIImportError(TVMCLIException):
    """TVMCLI TVMCLIImportError"""


from . import main
from . import compiler
from . import tunner
from . import runner
from .frontends import load_model as load
from .compiler import compile_model as compile
from .runner import run_module as run
from .tunner import tune_model as tune
from .model import TVMCLIModel, TVMCLIPackage, TVMCLIResult
