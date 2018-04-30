# Increase the chances that this code will work in both Python 2 and Python 3 (however, this is written for Python 3)
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import subprocess
import shlex

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

        self.tlm_observation = None  # type: SAMIObservation
        self.arc_observation = None  # type: SAMIObservation
        self.fiber_flat_observation = None  # type: SAMIObservation
        self.science_observation_list = None  # type: List[SAMIObservation}
        self.idx_file = None  # type: str

    def make_tramline_map(self):
        """

        aaorun reduce_fflat 14apr20026.fits -idxfile sami1000R.idx -OUT_DIRNAME 14apr20026_outdir -USEFLATIM 0

        """

        command = [
            "aaorun",
            "reduce_fflat",
            self.tlm_observation.raw_filename,
            "-idxfile " + self.idx_filename,
            "-USEFLATIM 0"
        ]

        subprocess.run(command)


    def reduce_arc(self):
        """
        aaorun reduce_arc 14apr20025red.fits -idxfile sami1000R.idx -OUT_DIRNAME 14apr20025_outdir -EXTR_OPERATION GAUSS -USEFLATIM 0 -TLMAP_FILENAME 14apr20026tlm.fits

        """

        command = "aaorun reduce_arc {arc_file} -idxfile {idx_file} -TLMAP_FILENAME {tlm_file}".format(
            arc_file=self.arc_observation.raw_filename,
            idx_file=self.idx_file,
            tlm_file=self.tlm_observation.reduced_filename
        )

        options = "-EXTR_OPERATION GAUSS -USEFLATIM 0"

        subprocess.run(shlex.split(command + " " + options))


    def reduce_fiber_flat(self):
        """
        aaorun reduce_fflat 14apr20026.fits -idxfile sami1000R.idx -OUT_DIRNAME 14apr20026_outdir -WAVEL_FILENAME 14apr20025red.fits
        """

        command = "aaorun reduce_fflat {fflat_file} -idxfile {idx_file} -WAVEL_FILENAME {arc_file}".format(
            fflat_file=self.fiber_flat_observation.raw_filename,
            idx_file=self.idx_file,
            arc_file=self.arc_observation.reduced_filename
        )
        subprocess.run(shlex.split(command))


    def reduce_objects(self):
        """Reduce all objects in this reduction group.

        Requires that previous reduction steps have already been run.

        """

        for science_obseration in self.science_observation_list:


            command = "aaorun reduce_object {science_file} -idxfile {idx_file} -TLMAP_FILENAME {tlm_file} -WAVEL_FILENAME {arc_file -FFLAT_FILENAME {fflat_file}".format(
                science_file=science_obseration.raw_filename,
                idx_file=self.idx_file,
                tlm_file=self.tlm_observation.tlm_filename

            )
            subprocess.run(shlex.split(command))


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

