import pytest

from glob import glob

import os
import tempfile
import shutil

import tdfdr

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "../sami_example_data/150422/ccd_2/")
ALL_DATA_DIR = os.path.join(os.path.dirname(__file__), "../sami_example_data/")

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
