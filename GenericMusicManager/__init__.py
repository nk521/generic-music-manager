from glob import glob
from pathlib import Path
from importlib import import_module
from typing import Callable
from GenericMusicManager.gmm import Music

mapped_url_sources: dict[str, Callable[[str], Music]] = dict()

for x in glob(str(Path(__file__).parent / "sources" / "*.py")):
    if x.endswith("__init__.py"):
        continue

    module_name = (x.split("/")[-1]).split(".")[0]
    imported_module = import_module(f"GenericMusicManager.sources.{module_name}")

    for var in (temp_vars := vars(imported_module)):
        if var.startswith("src_") and callable(temp_vars[var]):
            mapped_url_sources[imported_module.__url_regex__] = temp_vars[var]
    del imported_module

del import_module
del Path
del glob