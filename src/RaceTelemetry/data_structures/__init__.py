# RaceTelemetry/data_structures/__init__.py
"""Lazy-load metadata classes from each game struct module."""
from __future__ import annotations

import importlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Only seen by type checkers (Pylance/mypy), never runs.
    # This is what gives you hover info, autocomplete, and go-to-definition.
    from .AC_SM_struct import MetaData as AC_SM_MetaData
    from .AC_UDP_struct import MetaData as AC_UDP_MetaData
    from .ACC_struct import MetaData as ACC_MetaData
    from .ACE_struct import MetaData as ACE_MetaData
    from .BNG_struct import MetaData as BNG_MetaData
    from .Dirt_4_struct import MetaData as Dirt_4_MetaData
    from .Dirt_Rally_struct import MetaData as Dirt_Rally_MetaData
    from .ETS2_struct import MetaData as ETS2_MetaData
    from .F1_2016_struct import MetaData as F1_2016_MetaData
    from .F1_2017_struct import MetaData as F1_2017_MetaData
    from .F1_2018_struct import MetaData as F1_2018_MetaData
    from .F1_2019_struct import MetaData as F1_2019_MetaData
    from .F1_2020_struct import MetaData as F1_2020_MetaData
    from .F1_2021_struct import MetaData as F1_2021_MetaData
    from .F1_2022_struct import MetaData as F1_2022_MetaData
    from .F1_2023_struct import MetaData as F1_2023_MetaData
    from .F1_2024_struct import MetaData as F1_2024_MetaData
    from .F1_2025_struct import MetaData as F1_2025_MetaData
    from .F1_2026_struct import MetaData as F1_2026_MetaData
    from .FH4_struct import MetaData as FH4_MetaData
    from .FH5_struct import MetaData as FH5_MetaData
    from .FH6_struct import MetaData as FH6_MetaData
    from .FM7_struct import MetaData as FM7_MetaData
    from .FM8_struct import MetaData as FM8_MetaData
    from .GT7_struct import MetaData as GT7_MetaData
    from .IRacing_struct import MetaData as IRacing_MetaData
    from .PC2_struct import MetaData as PC2_MetaData
    from .PC_SM_struct import MetaData as PC_SM_MetaData
    from .PC_UDP_struct import MetaData as PC_UDP_MetaData

__all__ = [
    "AC_SM_MetaData",
    "AC_UDP_MetaData",
    "ACC_MetaData",
    "ACE_MetaData",
    "BNG_MetaData",
    "Dirt_4_MetaData",
    "Dirt_Rally_MetaData",
    "ETS2_MetaData",
    "F1_2016_MetaData",
    "F1_2017_MetaData",
    "F1_2018_MetaData",
    "F1_2019_MetaData",
    "F1_2020_MetaData",
    "F1_2021_MetaData",
    "F1_2022_MetaData",
    "F1_2023_MetaData",
    "F1_2024_MetaData",
    "F1_2025_MetaData",
    "F1_2026_MetaData",
    "FH4_MetaData",
    "FH5_MetaData",
    "FH6_MetaData",
    "FM7_MetaData",
    "FM8_MetaData",
    "GT7_MetaData",
    "IRacing_MetaData",
    "PC2_MetaData",
    "PC_SM_MetaData",
    "PC_UDP_MetaData",
]

_ALIASES = {
    "AC_SM_MetaData": "AC_SM_struct",
    "AC_UDP_MetaData": "AC_UDP_struct",
    "ACC_MetaData": "ACC_struct",
    "ACE_MetaData": "ACE_struct",
    "BNG_MetaData": "BNG_struct",
    "Dirt_4_MetaData": "Dirt_4_struct",
    "Dirt_Rally_MetaData": "Dirt_Rally_struct",
    "ETS2_MetaData": "ETS2_struct",
    "F1_2016_MetaData": "F1_2016_struct",
    "F1_2017_MetaData": "F1_2017_struct",
    "F1_2018_MetaData": "F1_2018_struct",
    "F1_2019_MetaData": "F1_2019_struct",
    "F1_2020_MetaData": "F1_2020_struct",
    "F1_2021_MetaData": "F1_2021_struct",
    "F1_2022_MetaData": "F1_2022_struct",
    "F1_2023_MetaData": "F1_2023_struct",
    "F1_2024_MetaData": "F1_2024_struct",
    "F1_2025_MetaData": "F1_2025_struct",
    "F1_2026_MetaData": "F1_2026_struct",
    "FH4_MetaData": "FH4_struct",
    "FH5_MetaData": "FH5_struct",
    "FH6_MetaData": "FH6_struct",
    "FM7_MetaData": "FM7_struct",
    "FM8_MetaData": "FM8_struct",
    "GT7_MetaData": "GT7_struct",
    "IRacing_MetaData": "IRacing_struct",
    "PC2_MetaData": "PC2_struct",
    "PC_SM_MetaData": "PC_SM_struct",
    "PC_UDP_MetaData": "PC_UDP_struct",
}


def __getattr__(name: str):
    """Lazy-load metadata classes on access."""
    if name not in _ALIASES:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    module_name = _ALIASES[name]
    module = importlib.import_module(f"{__name__}.{module_name}")
    return getattr(module, "MetaData")


def __dir__() -> list[str]:
    """List all available metadata classes."""
    return sorted(__all__)

