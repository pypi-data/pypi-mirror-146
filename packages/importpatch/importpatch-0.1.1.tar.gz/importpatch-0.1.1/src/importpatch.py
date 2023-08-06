from ast import parse
import atexit
import importlib
from importlib.abc import MetaPathFinder
from importlib.machinery import ModuleSpec, SourceFileLoader
from importlib.util import find_spec, spec_from_file_location
from pathlib import Path
import sys
import types
from typing import Sequence


MODULES_TO_PATCH: "dict[str,list[str]]" = {}
_FILE = Path(__file__)
_SHIM = _FILE.with_suffix(".pth")


class ImportPatchLoader(SourceFileLoader):
    def exec_module(self, module: types.ModuleType) -> None:
        super().exec_module(module)
        for src in MODULES_TO_PATCH.get(module.__name__, []):
            if find_spec(src):
                patcher = importlib.import_module(src)
                if hasattr(patcher, "patch"):
                    try:
                        patcher.patch(module)
                    except:
                        pass


class ImportPatchFinder(MetaPathFinder):
    def find_spec(
        self,
        fullname: str,
        path: "Sequence[str] | None",
        target: "types.ModuleType | None" = None,
    ) -> "ModuleSpec | None":
        if fullname in MODULES_TO_PATCH:
            if path is None or path == "":
                path = sys.path
            if "." in fullname:
                *parents, name = fullname.split(".")
            else:
                name = fullname
            for entry in path:
                name: Path = Path(entry).joinpath(name)
                if name.is_dir():
                    submodules = [name]
                    filename = name.joinpath("__init__.py")
                else:
                    filename = name.with_suffix(".py")
                    submodules = None
                if not filename.exists():
                    continue
                return spec_from_file_location(
                    fullname,
                    filename,
                    loader=ImportPatchLoader(fullname, filename),
                    submodule_search_locations=submodules,
                )
        return None


def inject():
    try:
        import json

        for path in [_FILE.parent, "~", "."]:
            path = Path(path).joinpath(".pymodpatch.json").expanduser().resolve()
            if path.exists():
                MODULES_TO_PATCH.update(json.loads(path.read_text()))
    except:
        pass
    sys.meta_path.insert(0, ImportPatchFinder())
    atexit.register(cleanup)


def cleanup():
    if not _FILE.exists():
        _SHIM.unlink(missing_ok=True)


def add(patch: str, src: "str"):
    srcs = MODULES_TO_PATCH.setdefault(patch, [])
    if src not in srcs:
        srcs.append(src)


def rm(patch: str, src: "str|None"):
    if src is None and patch in MODULES_TO_PATCH:
        MODULES_TO_PATCH[src].clear()
    elif src:
        srcs = MODULES_TO_PATCH.get(patch, [])
        while src in srcs:
            srcs.remove(src)


if __name__ == "__main__":

    # fmt: off
    def pth_import_fn():
        import importlib, atexit
        from importlib.util import find_spec
        from importlib import import_module
        from pathlib import Path
        import_module("importpatch").inject() if find_spec("importpatch") else None
        file = Path(locals().get("fullname"))
        atexit.register(lambda: file.unlink(missing_ok=True) if not file.with_suffix(".py").exists() else None)

    # fmt: on
    import argparse, inspect

    parser = argparse.ArgumentParser(description="Globals actions for ImportPatch")
    subparsers = parser.add_subparsers(title="Commands", dest="cmd")
    subparsers.add_parser(
        "enable", help=f"Add importpatch.pth to site-packages at: {_SHIM.parent}"
    )
    subparsers.add_parser(
        "disable", help=f"Remove importpatch.pth from site-packages at: {_SHIM.parent}"
    )
    args = parser.parse_args()
    if args.cmd == "enable":
        _SHIM.unlink(missing_ok=True)
        _SHIM.write_text(
            ";".join(inspect.getsource(pth_import_fn).splitlines()[1:]).strip()
        )
    elif args.cmd == "disable":
        _SHIM.unlink(missing_ok=True)
