# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 16:21:06 2021

@author: jpeacock
"""

# =============================================================================
# Imports
# =============================================================================
import numpy as np

from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from .standards import SCHEMA_FN_PATHS

# =============================================================================
attr_dict = get_schema("emeasurement", SCHEMA_FN_PATHS)

# ==============================================================================
# magnetic measurements
# ==============================================================================
class EMeasurement(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):

        self._fmt_dict = {
            "id": "<",
            "chtype": "<",
            "x": "<.2f",
            "y": "<.2f",
            "z": "<.2f",
            "x2": "<.2f",
            "y2": "<.2f",
            "z2": "<.2f",
            "acqchan": "<",
        }

        super().__init__(attr_dict=attr_dict, **kwargs)

    def __str__(self):
        return "\n".join([f"{k} = {v}" for k, v in self.to_dict(single=True).items()])

    def __repr__(self):
        return self.__str__()

    @property
    def dipole_length(self):
        if hasattr(self, "z"):
            return np.sqrt(
                (self.x2 - self.x) ** 2 + (self.y2 - self.y) ** 2 + self.z ** 2
            )
        else:
            return np.sqrt((self.x2 - self.x) ** 2 + (self.y2 - self.y) ** 2)

    @property
    def azimuth(self):
        if hasattr(self, "azm"):
            return self.azm
        try:
            return np.rad2deg(np.arctan2((self.y2 - self.y), (self.x2 - self.x)))
        except ZeroDivisionError:
            return 0.0

    @property
    def channel_number(self):
        if self.acqchan != None:
            if not isinstance(self.acqchan, (int, float)):
                try:
                    return [int("".join(i for i in self.acqchan if i.isdigit()))][0]
                except (IndexError, ValueError):
                    return 0
            return self.acqchan
        return 0
