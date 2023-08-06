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
""" Product Factory, class creating products according to their names """

from __future__ import annotations

import importlib
import logging
import re
from enum import unique
from pathlib import Path
from typing import Union
from zipfile import BadZipFile

from cloudpathlib import AnyPath, CloudPath
from sertit import files, strings
from sertit.misc import ListEnum

from eoreader.utils import EOREADER_NAME

LOGGER = logging.getLogger(EOREADER_NAME)


@unique
class CheckMethod(ListEnum):
    """Methods to recognize a product"""

    MTD = "Metadata"
    """Check the metadata: faster method"""

    NAME = "Filename"
    """
    Check the filename:

    Safer method that allows modified product names as it recursively looks for the metadata name in the product files.
    For products that have generic metadata files (ie. RS2 that as mtd named :code:`product.xml`),
    it also checks the band name.
    """

    BOTH = "Both"
    """Check the metadata and the filename: Double check if you have a doubt."""


@unique
class Platform(ListEnum):
    """Platforms supported by EOReader"""

    S1 = "Sentinel-1"
    """Sentinel-1"""

    S2 = "Sentinel-2"
    """Sentinel-2"""

    S2_THEIA = "Sentinel-2 Theia"
    """Sentinel-2 Theia"""

    S3_OLCI = "Sentinel-3 OLCI"
    """Sentinel-3 OLCI"""

    S3_SLSTR = "Sentinel-3 SLSTR"
    """Sentinel-3 SLSTR"""

    L9 = "Landsat-9"
    """Landsat-9"""

    L8 = "Landsat-8"
    """Landsat-8"""

    L7 = "Landsat-7"
    """Landsat-7"""

    L5 = "Landsat-5"
    """Landsat-5"""

    L4 = "Landsat-4"
    """Landsat-4"""

    L3 = "Landsat-3"
    """Landsat-3"""

    L2 = "Landsat-2"
    """Landsat-2"""

    L1 = "Landsat-1"
    """Landsat-1"""

    PLA = "PlanetScope"
    """PlanetScope"""

    # RPD = "RapidEye"
    # """RapidEye"""
    #
    SKY = "SkySat"
    """SkySat"""

    CSK = "COSMO-SkyMed"
    """COSMO-SkyMed"""

    CSG = "COSMO-SkyMed 2nd Generation"
    """COSMO-SkyMed 2nd Generation"""

    TSX = "TerraSAR-X"
    """TerraSAR-X"""

    TDX = "TanDEM-X"
    """TanDEM-X"""

    PAZ = "PAZ SAR"
    """SEOSAR/PAZ SAR"""

    RS2 = "RADARSAT-2"
    """RADARSAT-2"""

    PLD = "Pleiades"
    """Pléiades"""

    PNEO = "Pleiades-Neo"
    """Pleiades-Néo"""

    SPOT7 = "Spot-7"
    """SPOT-7"""

    SPOT6 = "Spot-6"
    """SPOT-6"""

    VIS1 = "Vision-1"
    """Vision-1"""

    RCM = "RADARSAT-Constellation Mission"
    """RADARSAT-Constellation Mission"""

    MAXAR = "Maxar"
    """Maxar (not a real platform, but used as a template for every Maxar products)"""

    QB = "QuickBird"
    """QuickBird"""

    GE01 = "GeoEye-1"
    """GeoEye-1"""

    WV01 = "WorldView-1"
    """WorldView-1"""

    WV02 = "WorldView-2"
    """WorldView-2"""

    WV03 = "WorldView-3"
    """WorldView-3"""

    WV04 = "WorldView-4"
    """WorldView-4"""

    ICEYE = "ICEYE"
    """ICEYE"""

    SAOCOM = "SAOCOM-1"
    """SAOCOM-1"""

    CUSTOM = "CUSTOM"
    """Custom stack"""


PLATFORM_REGEX = {
    Platform.S1: r"S1[AB]_(IW|EW|SM|WV)_(RAW|SLC|GRD|OCN)[FHM_]_[0-2]S[SD][HV]_\d{8}T\d{6}_\d{8}T\d{6}_\d{6}_.{11}",
    Platform.S2: r"S2[AB]_MSIL(1C|2A)_\d{8}T\d{6}_N\d{4}_R\d{3}_T\d{2}\w{3}_\d{8}T\d{6}",
    Platform.S2_THEIA: r"SENTINEL2[AB]_\d{8}-\d{6}-\d{3}_L(2A|1C)_T\d{2}\w{3}_[CDH](_V\d-\d|)",
    Platform.S3_OLCI: r"S3[AB]_OL_[012]_\w{6}_\d{8}T\d{6}_\d{8}T\d{6}_\d{8}T\d{6}_\w{17}_\w{3}_[OFDR]_(NR|ST|NT)_\d{3}",
    Platform.S3_SLSTR: r"S3[AB]_SL_[012]_\w{6}_\d{8}T\d{6}_\d{8}T\d{6}_\d{8}T\d{6}_\w{17}_\w{3}_[OFDR]_(NR|ST|NT)_\d{3}",
    Platform.L9: r"LC09_L1(GT|TP)_\d{6}_\d{8}_\d{8}_\d{2}_(RT|T1|T2)",
    Platform.L8: r"LC08_L1(GT|TP)_\d{6}_\d{8}_\d{8}_\d{2}_(RT|T1|T2)",
    Platform.L7: r"LE07_L1(GT|TP|GS)_\d{6}_\d{8}_\d{8}_\d{2}_(RT|T1|T2)",
    Platform.L5: r"L[TM]05_L1(TP|GS)_\d{6}_\d{8}_\d{8}_\d{2}_(T1|T2)",
    Platform.L4: r"L[TM]04_L1(TP|GS)_\d{6}_\d{8}_\d{8}_\d{2}_(T1|T2)",
    Platform.L3: r"LM03_L1(TP|GS)_\d{6}_\d{8}_\d{8}_\d{2}_T2",
    Platform.L2: r"LM02_L1(TP|GS)_\d{6}_\d{8}_\d{8}_\d{2}_T2",
    Platform.L1: r"LM01_L1(TP|GS)_\d{6}_\d{8}_\d{8}_\d{2}_T2",
    Platform.PLA: r"\d{8}_\d{6}_(\d{2}_|)\w{4}",
    Platform.CSK: [
        r".+",  # Need to check inside as the folder does not have any recognizable name
        r"CSKS\d_(RAW|SCS|DGM|GEC|GTC)_[UB]_(HI|PP|WR|HR|S2)_"
        r"\w{2}_(HH|VV|VH|HV|CO|CH|CV)_[LR][AD]_[FS][NF]_\d{14}_\d{14}\.h5",
    ],
    Platform.CSG: [
        r".+",  # Need to check inside as the folder does not have any recognizable name
        r"CSG_SSAR\d_(RAW|SCS|DGM|GEC|GTC)_([UBF]|FQLK_B)_\d{4}_(S2[ABC]|D2[RSJ]|OQ[RS]|STR|SC[12]|PPS|QPS)_\d{3}"
        r"_(HH|VV|VH|HV)_[LR][AD]_[DPFR]_\d{14}_\d{14}\_\d_[FC]_\d{2}[NS]_Z\d{2}_[NFB]\d{2}.h5",
    ],
    Platform.TSX: r"(TSX|TDX|PAZ)1_SAR__(SSC|MGD|GEC|EEC)_([SR]E|__)___[SH][MCLS]_[SDTQ]_[SD]RA_\d{8}T\d{6}_\d{8}T\d{6}",
    Platform.TDX: r"TDX1_SAR__(SSC|MGD|GEC|EEC)_([SR]E|__)___[SH][MCLS]_[SDTQ]_[SD]RA_\d{8}T\d{6}_\d{8}T\d{6}",
    Platform.PAZ: r"PAZ1_SAR__(SSC|MGD|GEC|EEC)_([SR]E|__)___[SH][MCLS]_[SDTQ]_[SD]RA_\d{8}T\d{6}_\d{8}T\d{6}",
    Platform.RS2: r"RS2_(OK\d+_PK\d+_DK\d+_.{2,}_\d{8}_\d{6}|\d{8}_\d{6}_\d{4}_.{1,5})"
    r"(_(HH|VV|VH|HV)){1,4}_S(LC|GX|GF|CN|CW|CF|CS|SG|PG)(_\d{6}_\d{4}_\d{8}|)",
    Platform.PLD: r"IMG_PHR1[AB]_(P|MS|PMS|MS-N|MS-X|PMS-N|PMS-X)_\d{3}",
    Platform.PNEO: r"IMG_\d+_PNEO\d_(P|MS|PMS|MS-FS|PMS-FS)",
    Platform.SPOT7: r"IMG_SPOT7_(P|MS|PMS|MS-N|MS-X|PMS-N|PMS-X)_\d{3}_\w",
    Platform.SPOT6: r"IMG_SPOT6_(P|MS|PMS|MS-N|MS-X|PMS-N|PMS-X)_\d{3}_\w",
    Platform.VIS1: r"VIS1_(PAN|BUN|PSH|MS4)_.+_\d{2}-\d",
    Platform.RCM: r"RCM\d_OK\d+_PK\d+_\d_.{4,}_\d{8}_\d{6}(_(HH|VV|VH|HV|RV|RH)){1,4}_(SLC|GRC|GRD|GCC|GCD)",
    Platform.QB: r"\d{12}_\d{2}_P\d{3}_(MUL|PAN|PSH|MOS)",
    Platform.GE01: r"\d{12}_\d{2}_P\d{3}_(MUL|PAN|PSH|MOS)",
    Platform.WV01: r"\d{12}_\d{2}_P\d{3}_(MUL|PAN|PSH|MOS)",
    Platform.WV02: r"\d{12}_\d{2}_P\d{3}_(MUL|PAN|PSH|MOS)",
    Platform.WV03: r"\d{12}_\d{2}_P\d{3}_(MUL|PAN|PSH|MOS)",
    Platform.WV04: r"\d{12}_\d{2}_P\d{3}_(MUL|PAN|PSH|MOS)",
    Platform.MAXAR: r"\d{12}_\d{2}_P\d{3}_(MUL|PAN|PSH|MOS)",
    Platform.ICEYE: r"((SM|SL|SC|SLEA)[HW]*_\d{5,}|ICEYE_X\d_(SM|SL|SC|SLEA)H*_\d{5,}_\d{8}T\d{6})",
    Platform.SAOCOM: r".+EOL1[ABCD]SARSAO1[AB]\d+(-product|)",
}

MTD_REGEX = {
    Platform.S1: {
        "nested": 1,
        # File that can be found at any level (product/**/file)
        "regex": r".*s1[ab]-(iw|ew|sm|wv)\d*-(raw|slc|grd|ocn)-[hv]{2}-\d{8}t\d{6}-\d{8}t\d{6}-\d{6}-\w{6}-\d{3}\.xml",
    },
    Platform.S2: {"nested": 3, "regex": r"MTD_TL.xml"},
    Platform.S2_THEIA: rf"{PLATFORM_REGEX[Platform.S2_THEIA]}_MTD_ALL\.xml",
    Platform.S3_OLCI: r"Oa\d{2}_radiance.nc",
    Platform.S3_SLSTR: r"S\d_radiance_an.nc",
    Platform.L9: rf"{PLATFORM_REGEX[Platform.L9]}_MTL\.txt",
    Platform.L8: rf"{PLATFORM_REGEX[Platform.L8]}_MTL\.txt",
    Platform.L7: rf"{PLATFORM_REGEX[Platform.L7]}_MTL\.txt",
    Platform.L5: rf"{PLATFORM_REGEX[Platform.L5]}_MTL\.txt",
    Platform.L4: rf"{PLATFORM_REGEX[Platform.L4]}_MTL\.txt",
    Platform.L3: rf"{PLATFORM_REGEX[Platform.L3]}_MTL\.txt",
    Platform.L2: rf"{PLATFORM_REGEX[Platform.L2]}_MTL\.txt",
    Platform.L1: rf"{PLATFORM_REGEX[Platform.L1]}_MTL\.txt",
    Platform.PLA: {
        "nested": -1,  # File that can be found at any level (product/**/file)
        "regex": r"\d{8}_\d{6}_(\d{2}_|)\w{4}_[13][AB]_.*metadata.*\.xml",
    },
    Platform.CSK: rf"{PLATFORM_REGEX[Platform.CSK][1]}\.xml",
    Platform.CSG: rf"{PLATFORM_REGEX[Platform.CSG][1]}\.xml",
    Platform.TSX: rf"{PLATFORM_REGEX[Platform.TSX]}\.xml",
    Platform.TDX: rf"{PLATFORM_REGEX[Platform.TSX]}\.xml",
    Platform.PAZ: rf"{PLATFORM_REGEX[Platform.TSX]}\.xml",
    Platform.RS2: [
        r"product\.xml",  # Too generic name, check also a band
        r"imagery_[HV]{2}\.tif",
    ],
    Platform.PLD: r"DIM_PHR1[AB]_(P|MS|PMS|MS-N|MS-X|PMS-N|PMS-X)_\d{15}_(SEN|PRJ|ORT|MOS)_.{10,}\.XML",
    Platform.PNEO: r"DIM_PNEO\d_\d{15}_(P|MS|PMS|MS-FS|PMS-FS)_(SEN|PRJ|ORT|MOS)_.{9,}_._._._.\.XML",
    Platform.SPOT7: r"DIM_SPOT7_(P|MS|PMS|MS-N|MS-X|PMS-N|PMS-X)_\d{15}_(SEN|PRJ|ORT|MOS)_.{10,}\.XML",
    Platform.SPOT6: r"DIM_SPOT6_(P|MS|PMS|MS-N|MS-X|PMS-N|PMS-X)_\d{15}_(SEN|PRJ|ORT|MOS)_.{10,}\.XML",
    Platform.VIS1: r"DIM_VIS1_(PSH|MS4|PAN)_\d{14}_(PRJ|ORTP)_S\d{5,}_\d{4}_Meta\.xml",
    Platform.RCM: {
        "nested": 1,  # File that can be found at 1st folder level (product/*/file)
        "regex": [
            r"product\.xml",  # Too generic name, check also a band
            r"\d+_[RHV]{2}\.tif",
        ],
    },
    Platform.QB: r"\d{2}\w{3}\d{8}-.{4}(_R\dC\d|)-\d{12}_\d{2}_P\d{3}.TIL",
    Platform.GE01: r"\d{2}\w{3}\d{8}-.{4}(_R\dC\d|)-\d{12}_\d{2}_P\d{3}.TIL",
    Platform.WV01: r"\d{2}\w{3}\d{8}-.{4}(_R\dC\d|)-\d{12}_\d{2}_P\d{3}.TIL",
    Platform.WV02: r"\d{2}\w{3}\d{8}-.{4}(_R\dC\d|)-\d{12}_\d{2}_P\d{3}.TIL",
    Platform.WV03: r"\d{2}\w{3}\d{8}-.{4}(_R\dC\d|)-\d{12}_\d{2}_P\d{3}.TIL",
    Platform.WV04: r"\d{2}\w{3}\d{8}-.{4}(_R\dC\d|)-\d{12}_\d{2}_P\d{3}.TIL",
    Platform.MAXAR: r"\d{2}\w{3}\d{8}-.{4}(_R\dC\d|)-\d{12}_\d{2}_P\d{3}.TIL",
    Platform.ICEYE: r"ICEYE_(X\d{1,}_|)(SLC|GRD)_((SM|SL|SC)H*|SLEA)_\d{5,}_\d{8}T\d{6}\.xml",
    Platform.SAOCOM: r"S1[AB]_OPER_SAR_EOSSP__CORE_L1[A-D]_OL(F|VF)_\d{8}T\d{6}.xemt",
}


class Reader:
    """
    Factory class creating satellite products according to their names.

    It creates a singleton that you can call only one time per file.
    """

    def __init__(self):
        self._platform_regex = {}
        self._mtd_regex = {}
        self._mtd_nested = {}

        # Register platforms
        for platform, regex in PLATFORM_REGEX.items():
            self._platform_regex[platform] = self._compile(regex, prefix="", suffix="")

        # Register metadata
        for platform, regex in MTD_REGEX.items():
            if isinstance(regex, dict):
                self._mtd_regex[platform] = self._compile(
                    regex["regex"], prefix=".*", suffix=""
                )
                self._mtd_nested[platform] = regex["nested"]
            else:
                self._mtd_regex[platform] = self._compile(regex, prefix=".*", suffix="")
                self._mtd_nested[platform] = 0

    @staticmethod
    def _compile(regex: Union[str, list], prefix="^", suffix="&") -> list:
        """
        Compile regex or list of regex

        Args:
            regex (Union[str, list]): Regex in :code:`re` sense
            prefix (str): Prefix of regex, ^ by default (means start of the string)
            suffix (str): Prefix of regex, & by default (means end of the string)

        Returns:
            list: List of compiled pattern
        """

        def _compile_(regex_str: str):
            return re.compile(f"{prefix}{regex_str}{suffix}")

        # Case folder is not enough to identify the products (ie. COSMO Skymed)
        if isinstance(regex, list):
            comp = [_compile_(regex) for regex in regex]
        else:
            comp = [_compile_(regex)]

        return comp

    def open(
        self,
        product_path: Union[str, CloudPath, Path],
        archive_path: Union[str, CloudPath, Path] = None,
        output_path: Union[str, CloudPath, Path] = None,
        method: CheckMethod = CheckMethod.MTD,
        remove_tmp: bool = False,
        custom=False,
        **kwargs,
    ) -> "Product":  # noqa: F821
        """
        Open the product.

        .. code-block:: python

            >>> from eoreader.reader import Reader
            >>> path = r"S2A_MSIL1C_20200824T110631_N0209_R137_T30TTK_20200824T150432.SAFE.zip"
            >>> Reader().open(path)
            <eoreader.products.optical.s2_product.S2Product object at 0x000001984986FAC8>

        Args:
            product_path (Union[str, CloudPath, Path]): Product path
            archive_path (Union[str, CloudPath, Path]): Archive path
            output_path (Union[str, CloudPath, Path]): Output Path
            method (CheckMethod): Checking method used to recognize the products
            remove_tmp (bool): Remove temp files (such as clean or orthorectified bands...) when the product is deleted
            custom (bool): True if we want to use a custom stack

        Returns:
            Product: Correct products

        """
        product_path = AnyPath(product_path)
        if not product_path.exists():
            FileNotFoundError(f"Non existing product: {product_path}")

        if custom:
            from eoreader.products import CustomProduct

            prod = CustomProduct(
                product_path=product_path,
                archive_path=archive_path,
                output_path=output_path,
                remove_tmp=remove_tmp,
                **kwargs,
            )
        else:
            prod = None
            for platform in PLATFORM_REGEX.keys():
                if method == CheckMethod.MTD:
                    is_valid = self.valid_mtd(product_path, platform)
                elif method == CheckMethod.NAME:
                    is_valid = self.valid_name(product_path, platform)
                else:
                    is_valid = self.valid_name(
                        product_path, platform
                    ) and self.valid_mtd(product_path, platform)

                if is_valid:
                    sat_class = platform.name.lower() + "_product"

                    # Channel correctly the sensors to their generic files (just in case)
                    # TerraSAR-like sensors
                    if platform in [Platform.TDX, platform.PAZ]:
                        sat_class = "tsx_product"
                    # Maxar-like sensors
                    elif platform in [
                        Platform.QB,
                        Platform.GE01,
                        Platform.WV01,
                        Platform.WV02,
                        Platform.WV03,
                        Platform.WV04,
                    ]:
                        sat_class = "maxar_product"

                    # Manage both optical and SAR
                    try:
                        mod = importlib.import_module(
                            f"eoreader.products.sar.{sat_class}"
                        )
                    except ModuleNotFoundError:
                        mod = importlib.import_module(
                            f"eoreader.products.optical.{sat_class}"
                        )

                    class_ = getattr(mod, strings.snake_to_camel_case(sat_class))
                    prod = class_(
                        product_path=product_path,
                        archive_path=archive_path,
                        output_path=output_path,
                        remove_tmp=remove_tmp,
                        **kwargs,
                    )
                    break

        if not prod:
            LOGGER.warning(
                "There is no existing products in EOReader corresponding to %s",
                product_path,
            )

        return prod

    def valid_name(
        self, product_path: Union[str, CloudPath, Path], platform: Union[str, Platform]
    ) -> bool:
        """
        Check if the product's name is valid for the given satellite


        .. code-block:: python

            >>> from eoreader.reader import Reader, Platform
            >>> path = r"S2A_MSIL1C_20200824T110631_N0209_R137_T30TTK_20200824T150432.SAFE.zip"
            >>> With IDs
            >>> Reader().valid_name(path, "S1")
            False
            >>> Reader().valid_name(path, "S2")
            True

            >>> # With names
            >>> Reader().valid_name(path, "Sentinel-1")
            False
            >>> Reader().valid_name(path, "Sentinel-2")
            True

            >>> # With Platform
            >>> Reader().valid_name(path, Platform.S1)
            False
            >>> Reader().valid_name(path, Platform.S2)
            True

        Args:
            product_path (Union[str, CloudPath, Path]): Product path
            platform (str): Platform's name or ID

        Returns:
            bool: True if valid name

        """
        platform = Platform.convert_from(platform)[0]
        regex = self._platform_regex[platform]
        return is_filename_valid(product_path, regex)

    def valid_mtd(
        self, product_path: Union[str, CloudPath, Path], platform: Union[str, Platform]
    ) -> bool:
        """
        Check if the product's mtd is in the product folder/archive

        .. code-block:: python

            >>> from eoreader.reader import Reader, Platform
            >>> path = r"S2A_MSIL1C_20200824T110631_N0209_R137_T30TTK_20200824T150432.SAFE.zip"
            >>> With IDs
            >>> Reader().valid_mtd(path, "S1")
            False
            >>> Reader().valid_mtd(path, "S2")
            True

            >>> # With names
            >>> Reader().valid_mtd(path, "Sentinel-1")
            False
            >>> Reader().valid_mtd(path, "Sentinel-2")
            True

            >>> # With Platform
            >>> Reader().valid_mtd(path, Platform.S1)
            False
            >>> Reader().valid_mtd(path, Platform.S2)
            True

        Args:
            product_path (Union[str, CloudPath, Path]): Product path
            platform (Union[str, Platform]): Platform's name or ID

        Returns:
            bool: True if valid name

        """
        # Convert platform if needed
        platform = Platform.convert_from(platform)[0]

        product_path = AnyPath(product_path)

        if not product_path.exists():
            return False

        # Here the list is a check of several files
        regex_list = self._mtd_regex[platform]
        nested = self._mtd_nested[platform]

        # False by default
        is_valid = [False for idx in regex_list]

        # Folder
        if product_path.is_dir():
            if nested < 0:
                prod_files = list(product_path.glob("**/*.*"))
            elif nested == 0:
                prod_files = list(
                    path for path in product_path.iterdir() if path.is_file()
                )
            else:
                nested_wildcard = "/".join(["*" for i in range(nested)])
                prod_files = list(product_path.glob(f"*{nested_wildcard}/*.*"))

        # Archive
        else:
            try:
                prod_files = files.get_archived_file_list(product_path)
            except BadZipFile:
                raise BadZipFile(f"{product_path} is not a zip file")

        # Check
        for idx, regex in enumerate(regex_list):
            for prod_file in prod_files:
                if regex.match(str(prod_file)):
                    is_valid[idx] = True
                    break

        return all(is_valid)


def is_filename_valid(
    product_path: Union[str, CloudPath, Path], regex: Union[list, re.Pattern]
) -> bool:
    """
    Check if the filename corresponds to the given satellite regex.

    Checks also if a file inside the directory is correct.

    .. WARNING::
        Two level max for the moment

    Args:
        product_path (Union[str, CloudPath, Path]): Product path
        regex (Union[list, re.Pattern]): Regex or list of regex

    Returns:
        bool: True if the filename corresponds to the given satellite regex
    """
    product_path = AnyPath(product_path)
    product_file_name = files.get_filename(product_path)

    # Case folder is not enough to identify the products (ie. COSMO Skymed)
    # WARNING: Two level max for the moment
    is_valid = bool(regex[0].match(product_file_name))
    if is_valid and len(regex) > 1:
        is_valid = False  # Reset
        if product_path.is_dir():
            file_list = product_path.iterdir()
            for file in file_list:
                if regex[1].match(file.name):
                    is_valid = True
                    break
        else:
            try:
                file_list = files.get_archived_file_list(product_path)
                for file in file_list:
                    if regex[1].match(file):
                        is_valid = True
                        break
            except TypeError:
                LOGGER.debug(
                    f"The product {product_file_name} should be a folder or an archive (.tar or .zip)"
                )
            except BadZipFile:
                raise BadZipFile(f"{product_path} is not a zip file")

    return is_valid
