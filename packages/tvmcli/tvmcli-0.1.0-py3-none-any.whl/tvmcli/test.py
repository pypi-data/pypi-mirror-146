import tvm

from tvm._ffi import registry

all_configs = tvm.ir.transform.PassContext.list_configs()
supported_config_types = ("IntImm", "runtime.String")
supported_configs = [
    name for name in all_configs.keys() if all_configs[name]["type"] in supported_config_types
]
print(("\n").join(supported_configs) + "\n")

_prefix = "relay._transform."
global_funcs = registry.list_global_func_names()
pass_list = [
    p
    for p in global_funcs
    if p.startswith(_prefix)
]
print("\n".join(pass_list))

# import tvm
#
# from tvm.driver import tvmc
#
# model = tvmc.load('my_model.onnx')