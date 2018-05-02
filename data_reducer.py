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

        with fits.open(self.raw_filename) as fits_data:

            self.ndf_class = fits_data["STRUCT.MORE.NDF_CLASS"].data[0][0]

            self.plate_id = fits_data[0].header["PLATEID"]


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

    def all_observations(self):
        all_obs = set()
        all_obs.update(self.tramline_observations)
        all_obs.update(self.arc_observations)
        all_obs.update(self.flatfield_observations)
        all_obs.update(self.science_observations)
        return all_obs

    def import_new_observation(self, observation):
        # type: (SAMIObservation) -> None

        if observation.plate_id not in self.reduction_groups:
            self.reduction_groups[observation.plate_id] = SAMIReductionGroup(observation.plate_id, "sami1000R.idx")

        reduction_group = self.reduction_groups[observation.plate_id]

        # Classify observation based on NDF CLASS
        if observation.ndf_class == "MFFFF":
            self.tramline_observations.append(observation)

            if reduction_group.tlm_observation is None:
                reduction_group.tlm_observation = observation

            self.flatfield_observations.append(observation)

            if reduction_group.fiber_flat_observation is None:
                reduction_group.fiber_flat_observation = observation

        elif observation.ndf_class == "MFARC":
            self.arc_observations.append(observation)

            if reduction_group.arc_observation is None:
                reduction_group.arc_observation = observation

        elif observation.ndf_class == "MFOBJECT":
            self.science_observations.append(observation)

            if observation not in reduction_group.science_observation_list:
                reduction_group.science_observation_list.append(observation)


    def reduce_all(self):
        pass
