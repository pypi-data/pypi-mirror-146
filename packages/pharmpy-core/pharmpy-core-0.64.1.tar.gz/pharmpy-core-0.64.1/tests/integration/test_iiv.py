import shutil

import numpy as np
import pytest

from pharmpy import Model
from pharmpy.modeling import create_joint_distribution, run_tool, set_seq_zo_fo_absorption
from pharmpy.utils import TemporaryDirectoryChanger


@pytest.mark.parametrize(
    'no_of_models, best_model_name',
    [(4, 'iiv_block_structure_candidate1')],
)
def test_iiv_block_structure(tmp_path, testdata, no_of_models, best_model_name):
    with TemporaryDirectoryChanger(tmp_path):
        shutil.copy2(testdata / 'nonmem' / 'models' / 'mox2.mod', tmp_path)
        shutil.copy2(testdata / 'nonmem' / 'models' / 'mox_simulated_normal.csv', tmp_path)
        model_start = Model.create_model('mox2.mod')
        model_start.datainfo.path = tmp_path / 'mox_simulated_normal.csv'

        res = run_tool('iiv', 'brute_force_block_structure', model=model_start)

        assert len(res.summary_tool) == no_of_models + 1
        assert len(res.summary_models) == no_of_models + 1
        assert len(res.models) == no_of_models
        assert all(
            model.modelfit_results and not np.isnan(model.modelfit_results.ofv)
            for model in res.models
        )
        assert all(model.random_variables != model_start.random_variables for model in res.models)
        assert res.best_model.name == best_model_name
        rundir = tmp_path / 'iiv_dir1'
        assert rundir.is_dir()
        assert len(list((rundir / 'models').iterdir())) == no_of_models + 2
        assert (rundir / 'metadata.json').exists()


def test_iiv_no_of_etas(tmp_path, testdata):
    with TemporaryDirectoryChanger(tmp_path):
        shutil.copy2(testdata / 'nonmem' / 'models' / 'mox2.mod', tmp_path)
        shutil.copy2(testdata / 'nonmem' / 'models' / 'mox_simulated_normal.csv', tmp_path)
        model_start = Model.create_model('mox2.mod')
        model_start.datainfo.path = tmp_path / 'mox_simulated_normal.csv'

        res = run_tool('iiv', 'brute_force_no_of_etas', model=model_start)

        assert len(res.summary_tool) == 8
        assert len(res.summary_models) == 8
        assert len(res.models) == 7
        assert res.best_model.name == 'iiv_no_of_etas_candidate3'
        rundir = tmp_path / 'iiv_dir1'
        assert rundir.is_dir()
        assert len(list((rundir / 'models').iterdir())) == 9
        assert (rundir / 'metadata.json').exists()


@pytest.mark.filterwarnings("ignore::UserWarning")
@pytest.mark.parametrize(
    'iiv_as_fullblock, best_model_name',
    [(False, 'iiv_no_of_etas_candidate4'), (True, 'iiv_no_of_etas_candidate4')],
)
def test_iiv_no_of_etas_added_iiv(tmp_path, testdata, iiv_as_fullblock, best_model_name):
    with TemporaryDirectoryChanger(tmp_path):
        shutil.copy2(testdata / 'nonmem' / 'models' / 'mox2.mod', tmp_path)
        shutil.copy2(testdata / 'nonmem' / 'models' / 'mox_simulated_normal.csv', tmp_path)
        model_start = Model.create_model('mox2.mod')
        model_start.datainfo.path = tmp_path / 'mox_simulated_normal.csv'

        set_seq_zo_fo_absorption(model_start)
        res = run_tool(
            'iiv',
            'brute_force_no_of_etas',
            add_iivs=True,
            iiv_as_fullblock=iiv_as_fullblock,
            rankfunc='bic',
            model=model_start,
        )

        assert (len(res.start_model.random_variables['ETA(1)'].joint_names) > 0) is iiv_as_fullblock
        assert len(res.summary_tool) == 16
        assert len(res.summary_models) == 16
        assert len(res.models) == 15
        assert res.best_model.name == best_model_name
        rundir = tmp_path / 'iiv_dir1'
        assert rundir.is_dir()
        assert len(list((rundir / 'models').iterdir())) == 17
        assert (rundir / 'metadata.json').exists()


def test_iiv_no_of_etas_fullblock(tmp_path, testdata):
    with TemporaryDirectoryChanger(tmp_path):
        shutil.copy2(testdata / 'nonmem' / 'models' / 'mox2.mod', tmp_path)
        shutil.copy2(testdata / 'nonmem' / 'models' / 'mox_simulated_normal.csv', tmp_path)
        model_start = Model.create_model('mox2.mod')
        model_start.datainfo.path = tmp_path / 'mox_simulated_normal.csv'

        create_joint_distribution(model_start)
        res = run_tool('iiv', 'brute_force_no_of_etas', model=model_start)

        assert len(res.summary_tool) == 8
        assert len(res.summary_models) == 8
        assert len(res.models) == 7
        assert res.best_model.name == 'iiv_no_of_etas_candidate3'
        rundir = tmp_path / 'iiv_dir1'
        assert rundir.is_dir()
        assert len(list((rundir / 'models').iterdir())) == 9
        assert (rundir / 'metadata.json').exists()
