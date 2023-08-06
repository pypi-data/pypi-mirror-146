# -*- coding: utf-8 -*-
# Copyright 2022, SERTIT-ICube - France, https://sertit.unistra.fr/
# This file is part of eoreader project
#     https://github.com/sertit/eoreader
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Aliases for bands and indices, created in order to import just this file and not :code:`OpticalBandNames`, :code:`SarBandNames` and :code:`index`.

To use it, simply type:

.. code-block:: python

    >>> from eoreader.bands import *
    >>> GREEN
    <OpticalBandNames.GREEN: 'GREEN'>
    >>> HH
    <SarBandNames.HH: 'HH'>
    >>> NDVI
    <function NDVI at 0x00000261F6FFA950>
"""
# Module name begins with _ to not be imported with *
import typing as _tp

from eoreader.bands import index as _idx
from eoreader.bands.bands import CloudsBandNames as _clouds
from eoreader.bands.bands import DemBandNames as _dem
from eoreader.bands.bands import OpticalBandNames as _obn
from eoreader.bands.bands import SarBandNames as _sbn
from eoreader.exceptions import InvalidTypeError as _ite

__all__ = _idx.get_all_index_names()
__all__ += _obn.list_names()
__all__ += _sbn.list_names()
__all__ += _dem.list_names()
__all__ += _clouds.list_names()
__all__ += [
    "is_clouds",
    "is_dem",
    "is_index",
    "is_optical_band",
    "is_sar_band",
    "is_sat_band",
    "to_band",
    "to_str",
]

# -- OPTICAL BANDS --
CA = _obn.CA  # Coastal aerosol
BLUE = _obn.BLUE
GREEN = _obn.GREEN
YELLOW = _obn.YELLOW
RED = _obn.RED
VRE_1 = _obn.VRE_1
VRE_2 = _obn.VRE_2
VRE_3 = _obn.VRE_3
NIR = _obn.NIR
NARROW_NIR = _obn.NARROW_NIR
WV = _obn.WV  # Water vapour
SWIR_CIRRUS = _obn.SWIR_CIRRUS  # Optical band based on cirrus
SWIR_1 = _obn.SWIR_1
SWIR_2 = _obn.SWIR_2
TIR_1 = _obn.TIR_1
TIR_2 = _obn.TIR_2
PAN = _obn.PAN

# -- S3-SLSTR Additional bands --
S7 = _obn.S7
F1 = _obn.F1
F2 = _obn.F2

# -- S3-OCLI Additional bands --
Oa01 = _obn.Oa01
Oa02 = _obn.Oa02
Oa05 = _obn.Oa05
Oa09 = _obn.Oa09
Oa10 = _obn.Oa10
Oa13 = _obn.Oa13
Oa14 = _obn.Oa14
Oa15 = _obn.Oa15
Oa18 = _obn.Oa18
Oa19 = _obn.Oa19
Oa21 = _obn.Oa21

# -- SAR BANDS --
VV = _sbn.VV
VV_DSPK = _sbn.VV_DSPK
HH = _sbn.HH
HH_DSPK = _sbn.HH_DSPK
VH = _sbn.VH
VH_DSPK = _sbn.VH_DSPK
HV = _sbn.HV
HV_DSPK = _sbn.HV_DSPK
RH = _sbn.RH
RH_DSPK = _sbn.RH_DSPK
RV = _sbn.RV
RV_DSPK = _sbn.RV_DSPK

# -- INDICES --
RGI = _idx.RGI
NDVI = _idx.NDVI
TCBRI = _idx.TCBRI
TCGRE = _idx.TCGRE
TCWET = _idx.TCWET
NDRE2 = _idx.NDRE2
NDRE3 = _idx.NDRE3
GLI = _idx.GLI
GNDVI = _idx.GNDVI
RI = _idx.RI
NDGRI = _idx.NDGRI
CIG = _idx.CIG
NDMI = _idx.NDMI
DSWI = _idx.DSWI
SRSWIR = _idx.SRSWIR
RDI = _idx.RDI
NDWI = _idx.NDWI
BAI = _idx.BAI
BAIS2 = _idx.BAIS2
NBR = _idx.NBR
MNDWI = _idx.MNDWI
AWEInsh = _idx.AWEInsh
AWEIsh = _idx.AWEIsh
WI = _idx.WI
AFRI_1_6 = _idx.AFRI_1_6
AFRI_2_1 = _idx.AFRI_2_1
BSI = _idx.BSI
WV_WI = _idx.WV_WI
WV_VI = _idx.WV_VI
WV_SI = _idx.WV_SI
WV_BI = _idx.WV_BI
SI = _idx.SI
GVMI = _idx.GVMI
SBI = _idx.SBI
SCI = _idx.SCI
PANI = _idx.PANI
GRI = _idx.GRI
SAVI = _idx.SAVI
OSAVI = _idx.OSAVI
VARI = _idx.VARI
EVI = _idx.EVI
CI1 = _idx.CI1
CI2 = _idx.CI2
NDMI21 = _idx.NDMI21

# -- DEM --
DEM = _dem.DEM
SLOPE = _dem.SLOPE
HILLSHADE = _dem.HILLSHADE

# -- CLOUDS --
RAW_CLOUDS = _clouds.RAW_CLOUDS
CLOUDS = _clouds.CLOUDS
SHADOWS = _clouds.SHADOWS
CIRRUS = _clouds.CIRRUS  # Cirrus detected
ALL_CLOUDS = _clouds.ALL_CLOUDS


def is_clouds(clouds: _tp.Any) -> bool:
    """
    Returns True if we have a Clouds-related keyword

    .. code-block:: python

        >>> from eoreader.bands import *
        >>> is_clouds(NDVI)
        False
        >>> is_clouds(HH)
        False
        >>> is_clouds(GREEN)
        False
        >>> is_clouds(SLOPE)
        False
        >>> is_clouds(CLOUDS)
        True
    """
    try:
        is_valid = _clouds(clouds)
    except ValueError:
        is_valid = False
    return is_valid


def is_dem(dem: _tp.Any) -> bool:
    """
    Returns True if we have a DEM-related keyword

    .. code-block:: python

        >>> from eoreader.bands import *
        >>> is_dem(NDVI)
        False
        >>> is_dem(HH)
        False
        >>> is_dem(GREEN)
        False
        >>> is_dem(SLOPE)
        True
        >>> is_dem(CLOUDS)
        False
    """
    try:
        is_valid = _dem(dem)
    except ValueError:
        is_valid = False
    return is_valid


def is_index(idx: _tp.Any) -> bool:
    """
    Returns True if is an index function from the :code:`bands.index` module

    .. code-block:: python

        >>> from eoreader.bands import *
        >>> is_index(NDVI)
        True
        >>> is_index(HH)
        False
        >>> is_index(GREEN)
        False
        >>> is_index(SLOPE)
        False
        >>> is_index(CLOUDS)
        False

    Args:
        idx (Any): Anything that could be an index

    Returns:
        bool: True if the index asked is an index function (such as :code:`index.NDVI`)

    """
    if isinstance(idx, str):
        is_idx = idx in _idx.get_all_index_names()
    else:
        is_idx = (
            "index" in idx.__module__ and idx.__name__ in _idx.get_all_index_names()
        )
    return is_idx


def is_optical_band(band: _tp.Any) -> bool:
    """
    Returns True if is an optical band (from :code:`OpticalBandNames`)

    .. code-block:: python

        >>> from eoreader.bands import *
        >>> is_optical_band(NDVI)
        False
        >>> is_optical_band(HH)
        False
        >>> is_optical_band(GREEN)
        True
        >>> is_optical_band(SLOPE)
        False
        >>> is_optical_band(CLOUDS)
        False

    Args:
        band (Any): Anything that could be an optical band

    Returns:
        bool: True if the band asked is an optical band

    """
    try:
        is_valid = _obn(band)
    except ValueError:
        is_valid = False
    return is_valid


def is_sar_band(band: _tp.Any) -> bool:
    """
    Returns True if is a SAR band (from :code:`SarBandNames`)

    .. code-block:: python

        >>> from eoreader.bands import *
        >>> is_sar_band(NDVI)
        False
        >>> is_sar_band(HH)
        True
        >>> is_sar_band(GREEN)
        False
        >>> is_sar_band(SLOPE)
        False
        >>> is_sar_band(CLOUDS)
        False

    Args:
        band (Any): Anything that could be a SAR band

    Returns:
        bool: True if the band asked is a SAR band

    """
    try:
        is_valid = _sbn(band)
    except ValueError:
        is_valid = False
    return is_valid


def is_sat_band(band: _tp.Any) -> bool:
    """
    Returns True if is a band (from both :code:`SarBandNames` or :code:`OpticalBandNames`)

    .. code-block:: python

        >>> from eoreader.bands import *
        >>> is_sat_band(NDVI)
        False
        >>> is_sat_band(HH)
        True
        >>> is_sat_band(GREEN)
        True
        >>> is_sat_band(SLOPE)
        False
        >>> is_sat_band(CLOUDS)
        False

    Args:
        band (Any): Anything that could be a band

    Returns:
        bool: True if the band asked is a band

    """
    return is_sar_band(band) or is_optical_band(band)


def to_band(to_convert: list) -> list:
    """
    Convert a string (or real value) to any alias, band or index.

    You can pass the name or the value of the bands.

    .. code-block:: python

        >>> to_band(["NDVI", "GREEN", RED, "VH_DSPK", "SLOPE", DEM, "CLOUDS", CLOUDS])
        [<function NDVI at 0x00000154DDB12488>,
        <OpticalBandNames.GREEN: 'GREEN'>,
        <OpticalBandNames.RED: 'RED'>,
        <SarBandNames.VH_DSPK: 'VH_DSPK'>,
        <DemBandNames.SLOPE: 'SLOPE'>,
        <DemBandNames.DEM: 'DEM'>,
        <ClassifBandNames.CLOUDS: 'CLOUDS'>,
        <ClassifBandNames.CLOUDS: 'CLOUDS'>]

    Args:
        to_convert (list): Values to convert into band objects

    Returns:
        list: converted values

    """
    if not isinstance(to_convert, list):
        to_convert = [to_convert]

    bands = []
    for tc in to_convert:
        band_or_idx = None
        # Try legit types
        if isinstance(tc, str):
            # Try index
            if hasattr(_idx, tc):
                band_or_idx = getattr(_idx, tc)
            else:
                try:
                    band_or_idx = _sbn.convert_from(tc)[0]
                except TypeError:
                    try:
                        band_or_idx = _obn.convert_from(tc)[0]
                    except TypeError:
                        try:
                            band_or_idx = _dem.convert_from(tc)[0]
                        except TypeError:
                            try:
                                band_or_idx = _clouds.convert_from(tc)[0]
                            except TypeError:
                                pass

        elif is_index(tc) or is_sat_band(tc) or is_dem(tc) or is_clouds(tc):
            band_or_idx = tc

        # Store it
        if band_or_idx:
            bands.append(band_or_idx)
        else:
            raise _ite(f"Unknown band or index: {tc}")

    return bands


def to_str(to_convert: list) -> list:
    """
    Convert a string (or real value) to any alias, band or index.

    You can pass the name or the value of the bands.

    .. code-block:: python

        >>> to_str(["NDVI", "GREEN", RED, "VH_DSPK", "SLOPE", DEM, "CLOUDS", CLOUDS])
        ['NDVI', 'GREEN', 'RED', 'VH_DSPK', 'SLOPE', 'DEM', 'CLOUDS', 'CLOUDS']

    Args:
        to_convert (list): Values to convert into str

    Returns:
        list: str bands
    """
    if not isinstance(to_convert, list):
        to_convert = [to_convert]

    bands_str = []
    for tc in to_convert:
        if isinstance(tc, str):
            band_str = tc
        else:
            try:
                band_str = tc.name
            except AttributeError:
                band_str = tc.__name__

        bands_str.append(band_str)

    return bands_str
