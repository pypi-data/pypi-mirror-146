"""
Hoodat components
"""
import os

try:
    from kfp.v2.components import load_component_from_file
except ImportError:
    from kfp.components import load_component_from_file

__all__ = [
    "AddPyOp",
]

AddPyOp = load_component_from_file(
    os.path.join(os.path.dirname(__file__), "add_py/component.yaml")
)

AddPyOp2 = load_component_from_file(
    os.path.join(os.path.dirname(__file__), "add_py/component.yaml")
)
