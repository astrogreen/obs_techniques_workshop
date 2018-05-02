import pytest

from glob import glob

import os
import tempfile

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "../sami_example_data/150422/ccd_2/")

from data_reducer import *

@pytest.fixture("function")
def temporary_working_directory():
    dir = tempfile.mkdtemp()
    old_wd = os.getcwd()
    os.chdir(dir)
    yield dir
    os.chdir(old_wd)
    # shutil.rmtree(dir)

@pytest.fixture("function")
def temporary_working_directory_with_data():
    dir = tempfile.mkdtemp()
    data_dir = os.path.join(dir, "data")
    shutil.copytree(TEST_DATA_DIR, data_dir)
    old_wd = os.getcwd()
    os.chdir(data_dir)
    yield data_dir
    os.chdir(old_wd)
    # shutil.rmtree(dir)

def test_pytest_not_capturing_fds(pytestconfig):
    # Note: pytest must be run in sys capture mode, instead of file descriptor capture mode
    # otherwise calls to "aaorun" seem to fail. This next test ensures that is the case.
    print("If this test fails, then you must run pytest with the option '--capture=sys'.")
    assert pytestconfig.getoption("capture") == "sys"




def test_ndf_class_object():

    sami_obs = SAMIObservation(TEST_DATA_DIR + "22apr20074.fits")

    assert sami_obs.ndf_class == "MFFFF"


def test_new_observation_add_and_classify(temporary_working_directory_with_data):

    mngr = SAMIReductionManager()

    for f in glob("*.fits"):
        obs = SAMIObservation(f)

        mngr.import_new_observation(obs)

    assert len(mngr.science_observations) == 2
    assert len(mngr.arc_observations) == 1
    assert len(mngr.flatfield_observations) == 1
    assert len(mngr.tramline_observations) == 1

    assert len(mngr.all_observations()) == 4


    assert "Y14SAR3_P005_12T056_15T080" in mngr.reduction_groups
