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
Pleiades products.
See `here <www.engesat.com.br/wp-content/uploads/PleiadesUserGuide-17062019.pdf>`_
for more information.
"""
import logging

from eoreader.products import DimapBandCombination, DimapProduct
from eoreader.utils import EOREADER_NAME

LOGGER = logging.getLogger(EOREADER_NAME)


class PldProduct(DimapProduct):
    """
    Class of Pleiades products.
    See `here <www.engesat.com.br/wp-content/uploads/PleiadesUserGuide-17062019.pdf>`_
    for more information.
    """

    def _set_resolution(self) -> float:
        """
        Set product default resolution (in meters)
        """
        # Not Pansharpened images
        if self.band_combi in [
            DimapBandCombination.MS,
            DimapBandCombination.MS_X,
            DimapBandCombination.MS_N,
        ]:
            return 2.0
        # Pansharpened images
        else:
            return 0.5
