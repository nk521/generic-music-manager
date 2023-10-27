import dataclasses
from glob import glob
from pathlib import Path
from importlib import import_module
from typing import Callable
from GenericMusicManager.gmm import HandlersProtocol

mapped_url_sources: dict[str, HandlersProtocol] = dict()

for x in glob(str(Path(__file__).parent / "sources" / "*.py")):
    if x.endswith("__init__.py"):
        continue

    module_name = (x.split("/")[-1]).split(".")[0]
    imported_module = import_module(f"GenericMusicManager.sources.{module_name}")

    for var in (temp_vars := vars(imported_module)):
        if var.startswith("Handle") and dataclasses.is_dataclass(temp_vars[var]):
            handler_class: HandlersProtocol = temp_vars[var]
            mapped_url_sources[handler_class.url_regex()] = handler_class
    del imported_module

del import_module
del Path
del glob