import os
import shutil
from filecmp import dircmp

from sonotoria.jinja import template_folder

TEST_DEST = 'tests/test_tmp'

def reset_dest_folder():
    if os.path.exists(TEST_DEST):
        shutil.rmtree(TEST_DEST)
    os.mkdir(TEST_DEST)

def use_test_dest(ftest):
    reset_dest_folder()
    ftest()
    reset_dest_folder()

def same_res(res_folder):
    comp = dircmp(TEST_DEST, res_folder)
    assert len(comp.left_only) == 0
    assert len(comp.right_only) == 0
    assert len(comp.diff_files) == 0

@use_test_dest
def test_templating_default_values():
    # Given
    src = 'tests/test_files/src'

    # When
    template_folder(src, TEST_DEST)

    # Then
    same_res('tests/test_files/res_default')

@use_test_dest
def test_templating_overridden_names():
    # Given
    src = 'tests/test_files/src'

    # When
    template_folder(src, TEST_DEST, context={'names':['chaest', 'polkka']})

    # Then
    same_res('tests/test_files/res_override')
