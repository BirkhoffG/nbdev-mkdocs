# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/Doc_Links_Utils.ipynb.

# %% auto 0
__all__ = ['fix_sym_links']

# %% ../../nbs/Doc_Links_Utils.ipynb 1
import importlib
import re
from typing import *

from nbdev.doclinks import NbdevLookup
from fastcore.basics import merge
from fastcore.foundation import L

# %% ../../nbs/Doc_Links_Utils.ipynb 3
def _get_backtick_enclosed_string(s: str) -> str:
    """Get the string enclosed in backticks.

    Args:
        s: The string to extract from

    Returns:
        The extracted string enclosed in backticks.

    !!! note

        The above docstring is autogenerated by docstring-gen library (https://docstring-gen.airt.ai)
    """
    pattern = r"`(.*?)`"
    match = re.search(pattern, s)
    return match.group(1)  # type: ignore

# %% ../../nbs/Doc_Links_Utils.ipynb 5
def _get_sym_path_from_nbdev_lookup(nbdev_lookup: NbdevLookup, symbol_details: Tuple[str, str, str]) -> str:  # type: ignore
    """Get the symbol path from the NbdevLookup instance

    Args:
        nbdev_lookup: Instance of NbdevLookup
        symbol_details: The details of the symbol returned by the NbdevLookup instance

    Returns:
        The matched symbol path

    !!! note

        The above docstring is autogenerated by docstring-gen library (https://docstring-gen.airt.ai)
    """
    py_syms = merge(
        *L(o["syms"].values() for o in nbdev_lookup.entries.values()).concat()
    )
    ret_val: List[str] = [
        key for key, value in py_syms.items() if value == symbol_details
    ]
    return ret_val[0]

# %% ../../nbs/Doc_Links_Utils.ipynb 8
def _import_symbol(symbol: str) -> Any:
    """Import the given symbol.

    Args:
        symbol: The symbol to import.

    Returns:
        The imported symbol.

    Raises:
        ModuleNotFoundError: If the module is not found.

    !!! note

        The above docstring is autogenerated by docstring-gen library (https://docstring-gen.airt.ai)
    """
    names = symbol.split(".")
    for i in range(len(names), 0, -1):
        try:
            module_name = ".".join(names[:i])
            # nosemgrep: python.lang.security.audit.non-literal-import.non-literal-import
            module = importlib.import_module(module_name)
            o = module
            for name in names[i:]:
                o = getattr(o, name)
            return o
        except ModuleNotFoundError:
            continue
    raise ModuleNotFoundError(f"ModuleNotFound: {symbol}")

# %% ../../nbs/Doc_Links_Utils.ipynb 18
def _get_current_docs_version(docs_versioning: str, lib_version: str) -> str:
    """Get the current docs version.

    Args:
        docs_versioning: The value set for docs_versioning flag in settings.ini file.
        lib_version: The current version of the library.

    Returns:
        The current docs version.

    !!! note

        The above docstring is autogenerated by docstring-gen library (https://docstring-gen.airt.ai)
    """
    return (
        ".".join(lib_version.split(".")[:-1])
        if docs_versioning == "minor" and lib_version.replace(".", "").isdigit()
        else lib_version
    )

# %% ../../nbs/Doc_Links_Utils.ipynb 23
def _append_doc_version(fixed_part: str, docs_versioning: str, lib_version: str) -> str:
    """Append the current version of the documentation to a URL.

    Args:
        fixed_part: The fixed part of the URL.
        docs_versioning: The value set for docs_versioning flag in settings.ini file.
        lib_version: The version of the library.

    Returns:
        The URL with the documentation version appended.

    !!! note

        The above docstring is autogenerated by docstring-gen library (https://docstring-gen.airt.ai)
    """
    return (
        f"{fixed_part}/{_get_current_docs_version(docs_versioning, lib_version)}"
        if docs_versioning != "" and docs_versioning != "None"
        else fixed_part
    )

# %% ../../nbs/Doc_Links_Utils.ipynb 28
def _get_relative_sym_path(o: Any) -> str:
    """Get the relative path of a symbol

    Args:
        o: The symbol to get the relative path of

    Returns:
        The relative path of the symbol

    !!! note

        The above docstring is autogenerated by docstring-gen library (https://docstring-gen.airt.ai)
    """
    qualname = o.__qualname__.split(".")
    _o = (
        o
        if len(qualname) == 1
        else _import_symbol(o.__module__ + "." + o.__qualname__.split(".")[0])
    )
    return "/".join((_o.__module__ + "." + _o.__qualname__).split("."))

# %% ../../nbs/Doc_Links_Utils.ipynb 36
def _update_link(  # type: ignore
    symbol: str,
    symbol_details: Tuple[str, str, str],
    nbdev_lookup: NbdevLookup,
    docs_versioning: str,
    lib_version: str,
    use_relative_doc_links: bool,
) -> str:
    """Update the link of a symbol

    Args:
        symbol: The symbol to update
        symbol_details: The details of the symbol returned by the NbdevLookup instance
        nbdev_lookup: Instance of the NbdevLookup class
        docs_versioning: The value set for docs_versioning flag in settings.ini file
        lib_version: The current version of the library
        use_relative_doc_links: If set to True, relative link to symbols will be add in the generated
            documentation for easier local navigation

    Returns:
        The updated link

    !!! note

        The above docstring is autogenerated by docstring-gen library (https://docstring-gen.airt.ai)
    """
    fixed_part = "/".join(symbol_details[0].split("/")[:4])
    fixed_part_with_docs_version = _append_doc_version(
        fixed_part, docs_versioning, lib_version
    )

    full_symbol_path = _get_sym_path_from_nbdev_lookup(nbdev_lookup, symbol_details)
    o = _import_symbol(full_symbol_path)
    relative_sym_path = _get_relative_sym_path(o)
    if use_relative_doc_links:
        updated_link = f"[`{symbol}`](api/{relative_sym_path}/#{o.__module__ + '.' + o.__qualname__})"
    else:
        updated_link = f"[`{symbol}`]({fixed_part_with_docs_version}/api/{relative_sym_path}/#{o.__module__ + '.' + o.__qualname__})"

    return updated_link

# %% ../../nbs/Doc_Links_Utils.ipynb 42
def fix_sym_links(s: str, nbdev_lookup: NbdevLookup, docs_versioning: str, lib_version: str, use_relative_doc_links: bool) -> str:  # type: ignore
    """Fix the default sym links generated by nbdev in the given string.

    Args:
        s: The string to fix
        nbdev_lookup: Instance of the NbdevLookup class.
        docs_versioning: The value set for docs_versioning flag in settings.ini file.
        lib_version: The current version of the library.
        use_relative_doc_links: If set to True, relative link to symbols will be add in the generated
            documentation for easier local navigation.

    Returns:
        The string with correct links added to the symbol references.

    !!! note

        The above docstring is autogenerated by docstring-gen library (https://docstring-gen.airt.ai)
    """
    pattern = r"\[`.+?`\]\(https?://[^)]+\)"
    for match in re.findall(pattern, s):
        symbol = _get_backtick_enclosed_string(match)
        symbol_details = nbdev_lookup[symbol]
        if symbol_details is not None:
            updated_link = _update_link(
                symbol,
                symbol_details,
                nbdev_lookup,
                docs_versioning,
                lib_version,
                use_relative_doc_links,
            )
            s = s.replace(match, updated_link)
    return s
