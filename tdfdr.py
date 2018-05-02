from __future__ import absolute_import, division, print_function, unicode_literals

import subprocess
import os
import shutil, shlex


# Set up logging
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


# Check that 2dfdr is available.
try:
    subprocess.run(["aaorun", "help"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    tdfdr_is_available = False
except subprocess.CalledProcessError:
    print('Cannot find the 2dfdr executable `aaorun`\n'
          + 'Please ensure that 2dfdr is correctly installed.')
    tdfdr_is_available = False
else:
    tdfdr_is_available = True
    try:
        assert len(os.environ["DISPLAY"]) > 0
    except (AssertionError, TypeError):
        print("2dfdr requires a working DISPLAY. If you are running remotely, try enabling X-forwarding.")
        tdfdr_is_available = False



def aaorun(operation, files, idx_file, arc_file=None, tlm_file=None, fiber_flat_file=None):

    # Check valid operation
    if operation not in [
        "make_ex",
        "make_red",
        "make_im",
        "reduce_object",
        "combine_image",
        "splice",
        "reduce_run",
        "reduce_sky",
        "reduce_dark",
        "nop2",
        "reduce_fflux",
        "reduce_lflat",
        "reduce_bias",
        "reduce_fflat",
        "reduce_arc",
        "combine_spectra",
        "sourcefile",
        "combine_spectra_old",
        "make_tlm",
        "transfunc",
        "version",
        "clean",
        "get",
        "assimilate",
        "list",
        "examples",
        "getkywd",
        "compare",
        "help"
    ]:
        raise ValueError("%s is not a valid aaorun operation." % operation)

    command = ["aaorun"]

    command.append(operation)

    command.append(files)

    if not idx_file.endswith(".idx"):
        raise ValueError("idx filename must have the extension `.idx`")

    command.extend(["-idxFile", idx_file])


    if tlm_file:
        command.extend(["-TLMAP_FILENAME", tlm_file])

    if arc_file:
        command.extend(["-WAVEL_FILENAME", arc_file])

    if fiber_flat_file:
        command.extend(["-FFLAT_FILENAME", fiber_flat_file])

    log.info(" ".join(command))

    if tdfdr_is_available:
        return subprocess.run(command, check=True, timeout=300)
    else:
        print(" ".join(command))
        return " ".join(command)
