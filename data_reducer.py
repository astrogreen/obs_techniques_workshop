# Increase the chances that this code will work in both Python 2 and Python 3 (however, this is written for Python 3)
from __future__ import absolute_import, division, print_function, unicode_literals

import os

from typing import *

from astropy.io import fits



class SAMIObservation(object):

    def __init__(self, raw_filename):

        self.is_reduced = False

        self.raw_filename = raw_filename

        self.provenance_data = {}

class SAMIReductionGroup(object):
    """Collect together matched calibrations and science observations"""

    def __init__(self):

        self.tlm_observation = None
        self.arc_observation = None
        self.fiber_flat_observation = None
        self.science_observation_list = None

    def make_tramline_map(self):
        pass

    def reduce_arc(self):
        pass

    def fiber_flat_arc(self):
        pass

    def reduce_object(self):
        pass


class SAMIReductionManager(object):

    def __init__(self, working_directory):

        self.tramline_observations = []
        self.arc_observations = []
        self.flatfield_observations = []
        self.science_observations = []
        self.reduction_groups = []  # type: List[SAMIReductionGroup]

    def import_new_observation(self, observation):
        pass

    def reduce_all(self):
        pass

