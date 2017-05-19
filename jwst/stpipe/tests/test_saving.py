"""Test step/pipeline saving"""

from __future__ import absolute_import, division, print_function

import os
from os.path import (
    dirname,
    isfile,
    join,
    splitext,
)
import shutil
import tempfile

import pytest

from ..step import Step


@pytest.fixture
def mk_tmp_dirs():
    tmp_current_path = tempfile.mkdtemp()
    tmp_data_path = tempfile.mkdtemp()
    tmp_config_path = tempfile.mkdtemp()

    old_path = os.getcwd()
    try:
        os.chdir(tmp_current_path)
        yield (tmp_current_path, tmp_data_path, tmp_config_path)
    finally:
        os.chdir(old_path)


def test_save_step_default(mk_tmp_dirs):
    """Default save should be current working directory"""
    tmp_current_path, tmp_data_path, tmp_config_path = mk_tmp_dirs
    orig_filename = join(dirname(__file__), 'data', 'flat.fits')
    temp_filename = join(tmp_data_path, 'flat.fits')
    shutil.copyfile(orig_filename, temp_filename)

    args = [
        'jwst.stpipe.tests.steps.StepWithModel',
        temp_filename
    ]

    Step.from_cmdline(args)

    fname = 'flat_StepWithModel.fits'
    assert isfile(fname)


def test_save_pipeline_default(mk_tmp_dirs):
    """Default save should be current working directory"""
    tmp_current_path, tmp_data_path, tmp_config_path = mk_tmp_dirs
    step_fn = 'save_pipeline.cfg'
    data_fn = 'flat.fits'
    data_name, data_ext = splitext(data_fn)

    step_fn_path = join(dirname(__file__), 'steps', step_fn)
    data_fn_path = join(dirname(__file__), 'data', data_fn)

    tmp_step_fn_path = join(tmp_config_path, step_fn)
    tmp_data_fn_path = join(tmp_data_path, data_fn)
    shutil.copy(step_fn_path, tmp_step_fn_path)
    shutil.copy(data_fn_path, tmp_data_fn_path)

    args = [
        step_fn_path,
        tmp_data_fn_path,
        '--steps.savestep.skip=False'
    ]

    Step.from_cmdline(args)

    output_pipeline_fn_path = data_name + '_processed_SavePipeline' + data_ext
    output_stepsave_fn_path = data_name + '_processed' + data_ext
    assert isfile(output_pipeline_fn_path)
    assert isfile(output_stepsave_fn_path)


def test_save_step_specified(mk_tmp_dirs):
    """Save to specified folder"""
    tmp_current_path, tmp_data_path, tmp_config_path = mk_tmp_dirs
    orig_filename = join(dirname(__file__), 'data', 'flat.fits')

    args = [
        'jwst.stpipe.tests.steps.StepWithModel',
        orig_filename,
        '--output_dir=' + tmp_data_path
    ]

    Step.from_cmdline(args)

    output_fn_path = join(tmp_data_path, 'flat_StepWithModel.fits')
    assert isfile(output_fn_path)


def test_save_pipeline_specified(mk_tmp_dirs):
    """Save to specified folder"""
    tmp_current_path, tmp_data_path, tmp_config_path = mk_tmp_dirs
    step_fn = 'save_pipeline.cfg'
    data_fn = 'flat.fits'
    data_name, data_ext = splitext(data_fn)

    step_fn_path = join(dirname(__file__), 'steps', step_fn)
    data_fn_path = join(dirname(__file__), 'data', data_fn)

    tmp_step_fn_path = join(tmp_config_path, step_fn)
    shutil.copy(step_fn_path, tmp_step_fn_path)

    args = [
        step_fn_path,
        data_fn_path,
        '--output_dir=' + tmp_data_path,
    ]

    Step.from_cmdline(args)

    output_pipeline_fn_path = join(
        tmp_data_path,
        data_name + '_SavePipeline' + data_ext
    )
    assert isfile(output_pipeline_fn_path)


def test_save_substep_specified(mk_tmp_dirs):
    """Save to specified folder"""
    tmp_current_path, tmp_data_path, tmp_config_path = mk_tmp_dirs
    step_fn = 'save_pipeline.cfg'
    data_fn = 'flat.fits'
    data_name, data_ext = splitext(data_fn)

    step_fn_path = join(dirname(__file__), 'steps', step_fn)
    data_fn_path = join(dirname(__file__), 'data', data_fn)

    tmp_step_fn_path = join(tmp_config_path, step_fn)
    shutil.copy(step_fn_path, tmp_step_fn_path)

    args = [
        step_fn_path,
        data_fn_path,
        '--steps.savestep.skip=False',
        '--steps.savestep.output_dir=' + tmp_data_path
    ]

    Step.from_cmdline(args)

    output_pipeline_fn_path = data_name + '_processed_SavePipeline' + data_ext
    output_stepsave_fn_path = join(
        tmp_data_path,
        data_name + '_processed' + data_ext
    )
    assert isfile(output_pipeline_fn_path)
    assert isfile(output_stepsave_fn_path)


def test_save_proper_pipeline(mk_tmp_dirs):
    """Test how pipeline saving should work"""

    data_fn = 'flat.fits'
    data_name, data_ext = splitext(data_fn)
    data_fn_path = join(dirname(__file__), 'data', data_fn)

    args = [
        'jwst.stpipe.tests.steps.ProperPipeline',
        data_fn_path,
    ]
    Step.from_cmdline(args)

    assert isfile('ppbase_pp.fits')


def test_save_proper_pipeline_outputdir(mk_tmp_dirs):
    """Test how pipeline saving should work with output_dir"""
    tmp_current_path, tmp_data_path, tmp_config_path = mk_tmp_dirs

    data_fn = 'flat.fits'
    data_name, data_ext = splitext(data_fn)
    data_fn_path = join(dirname(__file__), 'data', data_fn)

    args = [
        'jwst.stpipe.tests.steps.ProperPipeline',
        data_fn_path,
        '--output_dir=' + tmp_data_path
    ]
    Step.from_cmdline(args)

    assert isfile(join(tmp_data_path, 'ppbase_pp.fits'))


def test_save_proper_pipeline_outputdir_outputname(mk_tmp_dirs):
    """Test how pipeline saving should work with output_dir"""
    tmp_current_path, tmp_data_path, tmp_config_path = mk_tmp_dirs

    data_fn = 'flat.fits'
    data_name, data_ext = splitext(data_fn)
    data_fn_path = join(dirname(__file__), 'data', data_fn)
    output_name = 'junk.fits'

    args = [
        'jwst.stpipe.tests.steps.ProperPipeline',
        data_fn_path,
        '--output_file=' + output_name,
        '--output_dir=' + tmp_data_path
    ]
    Step.from_cmdline(args)

    name, ext = splitext(output_name)
    pipeline_output = name + '_pp' + ext
    assert isfile(join(tmp_data_path, pipeline_output))


def test_save_proper_pipeline_substeps(mk_tmp_dirs):
    """Test how pipeline saving should work"""

    data_fn = 'flat.fits'
    data_name, data_ext = splitext(data_fn)
    data_fn_path = join(dirname(__file__), 'data', data_fn)

    args = [
        'jwst.stpipe.tests.steps.ProperPipeline',
        data_fn_path,
        '--steps.stepwithmodel.save_results=true',
        '--steps.another_stepwithmodel.save_results=true',
    ]
    Step.from_cmdline(args)

    assert isfile('ppbase_pp.fits')
    assert isfile('ppbase_swm.fits')
    assert isfile('ppbase_aswm.fits')


def test_save_proper_pipeline_substeps_outputdir(mk_tmp_dirs):
    """Test how pipeline saving should work"""
    tmp_current_path, tmp_data_path, tmp_config_path = mk_tmp_dirs

    data_fn = 'flat.fits'
    data_name, data_ext = splitext(data_fn)
    data_fn_path = join(dirname(__file__), 'data', data_fn)

    args = [
        'jwst.stpipe.tests.steps.ProperPipeline',
        data_fn_path,
        '--output_dir=' + tmp_data_path,
        '--steps.stepwithmodel.save_results=true',
        '--steps.another_stepwithmodel.save_results=true',
        '--steps.another_stepwithmodel.output_dir=' + tmp_config_path,
    ]
    Step.from_cmdline(args)

    assert isfile(join(tmp_data_path, 'ppbase_pp.fits'))
    assert isfile(join(tmp_data_path, 'ppbase_swm.fits'))
    assert isfile(join(tmp_config_path, 'ppbase_aswm.fits'))
