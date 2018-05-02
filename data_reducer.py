# Increase the chances that this code will work in both Python 2 and Python 3 (however, this is written for Python 3!!!)
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import shutil

from typing import *

from astropy.io import fits

from tdfdr import aaorun

import logging
log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)


class SAMIObservation(object):

    def __init__(self, raw_filename):

        self.is_reduced = False
        self.raw_filename = raw_filename
        self.provenance_data = {}


class SAMIReductionGroup(object):

    def __init__(self, plate_id, idx_file):

        self.tlm_observation = None  # type: SAMIObservation
        self.arc_observation = None  # type: SAMIObservation
        self.fiber_flat_observation = None  # type: SAMIObservation
        self.science_observation_list = []  # type: List[SAMIObservation}
        self.idx_file = idx_file  # type: str
        self.plate_id = plate_id  # type: str

    def make_tramline_map(self):
        pass

    def reduce_arc(self):
        pass

    def reduce_fiber_flat(self):
        pass

    def reduce_objects(self):
        pass


class SAMIReductionManager(object):

    def __init__(self):

        self.tramline_observations = []
        self.arc_observations = []
        self.flatfield_observations = []
        self.science_observations = []

        self.reduction_groups = {}  # type: Dict[str, SAMIReductionGroup]

    def import_new_observation(self, observation):
        pass

    def reduce_all(self):
        pass
