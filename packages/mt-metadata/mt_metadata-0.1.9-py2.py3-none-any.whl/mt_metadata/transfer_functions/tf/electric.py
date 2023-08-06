# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 21:30:36 2020

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""
# =============================================================================
# Imports
# =============================================================================
import numpy as np

from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema
from .standards import SCHEMA_FN_PATHS
from . import Electrode, Diagnostic, Channel

# =============================================================================
attr_dict = get_schema("electric", SCHEMA_FN_PATHS)
attr_dict.add_dict(get_schema("channel", SCHEMA_FN_PATHS))
dq_dict = get_schema("data_quality", SCHEMA_FN_PATHS)
dq_dict.add_dict(get_schema("rating", SCHEMA_FN_PATHS), "rating")
attr_dict.add_dict(dq_dict, "data_quality")
attr_dict.add_dict(get_schema("filtered", SCHEMA_FN_PATHS), "filter")
electrode_dict = get_schema("instrument", SCHEMA_FN_PATHS)
electrode_dict.add_dict(get_schema("location", SCHEMA_FN_PATHS), None)
attr_dict.add_dict(electrode_dict, "positive")
attr_dict.add_dict(electrode_dict, "negative")
attr_dict.add_dict(get_schema("time_period", SCHEMA_FN_PATHS), "time_period")
# =============================================================================
class Electric(Channel):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        self._dipole_length = 0.0
        self.positive = Electrode()
        self.negative = Electrode()
        self.contact_resistance = Diagnostic()
        self.ac = Diagnostic()
        self.dc = Diagnostic()
        self.units = None
        self.type = "electric"

        # must go after setting attributes otherwise Base won't find attribute
        # descriptions and throw an error
        Channel.__init__(self, **kwargs)
        self._attr_dict = attr_dict

    @property
    def dipole_length(self):
        return self._dipole_length

    @dipole_length.setter
    def dipole_length(self, value):
        try:
            value = float(value)
        except ValueError:
            raise ValueError("Input dipole length must be a float")

        self._dipole_length = value

        if self.translated_azimuth != None:
            self.positive.x2 = value * np.cos(np.deg2rad(self.translated_azimuth))
            self.positive.y2 = value * np.sin(np.deg2rad(self.translated_azimuth))
        else:
            self.positive.x2 = value * np.cos(np.deg2rad(self.measurement_azimuth))
            self.positive.y2 = value * np.sin(np.deg2rad(self.measurement_azimuth))
