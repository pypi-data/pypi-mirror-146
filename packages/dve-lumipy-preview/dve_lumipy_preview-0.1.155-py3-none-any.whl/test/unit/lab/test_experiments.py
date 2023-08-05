from lumipy.lab import Experiment, Convener
from test.unit.lab.mock_query import MockQuery
import unittest
from pathlib import Path
import pandas as pd
import os


class TestLumiLabExperiment(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.work_dir = '/tmp/lumi_unit_tests/'

        if os.path.exists(f'{cls.work_dir}/data/sequential.csv'):
            os.remove(f'{cls.work_dir}/data/sequential.csv')
        if os.path.exists(f'{cls.work_dir}/data/sequential_sp.csv'):
            os.remove(f'{cls.work_dir}/data/sequential_sp.csv')
        if os.path.exists(f'{cls.work_dir}/data/concurrent.csv'):
            os.remove(f'{cls.work_dir}/data/concurrent.csv')

        cls.path = Path(cls.work_dir)
        cls.path.mkdir(parents=True, exist_ok=True)

    @classmethod
    def tearDownClass(cls) -> None:
        if os.path.exists(f'{cls.work_dir}/data/sequential.csv'):
            os.remove(f'{cls.work_dir}/data/sequential.csv')
        if os.path.exists(f'{cls.work_dir}/data/concurrent.csv'):
            os.remove(f'{cls.work_dir}/data/concurrent.csv')
        if os.path.exists(f'{cls.work_dir}/data/sequential_sp.csv'):
            os.remove(f'{cls.work_dir}/data/sequential_sp.csv')

    def test_mock_query_job(self):

        build = MockQuery.build

        qry = build(5)

        self.assertEqual(qry.x, 5)
        self.assertEqual(qry.call_count, 0)

        job = qry.go_async()
        job.interactive_monitor()

        df = job.get_result()
        self.assertSequenceEqual(df.shape, [5, 3])
        self.assertEqual(qry.call_count, 1)

    def test_sequential_experiment(self):

        n_experiments = 5

        build_fn = MockQuery.build
        experiment = Experiment('sequential', build_fn, [1, 10], seed=1989)
        experiment_run = Convener(self.work_dir, experiment, n_experiments)
        experiment_run.go()

        df = pd.read_csv(experiment_run.data_file)

        self.assertEqual(df.shape[0], n_experiments)

        self.assertEqual(experiment.n_parallel, 1)
        self.assertEqual(experiment.name, 'sequential')
        self.assertEqual(experiment.quiet, False)
        self.assertEqual(experiment.seed, 1989 + n_experiments)
        self.assertEqual(experiment.ranges, ([1, 10], ))

        self.assertEqual(experiment_run.work_dir, self.work_dir)

    def test_sequential_single_point_experiment(self):

        n_experiments = 5

        build_fn = MockQuery.build
        experiment = Experiment('sequential_sp', build_fn, 10, seed=1989)
        experiment_run = Convener(self.work_dir, experiment, n_experiments)
        experiment_run.go()

        df = pd.read_csv(experiment_run.data_file)

        self.assertEqual(df.shape[0], n_experiments)

    def test_concurrent_experiment(self):

        n_experiments = 5
        n_parallel = 5

        build_fn = MockQuery.build
        experiment = Experiment('concurrent', build_fn, [1, 10], seed=1989, n_parallel=n_parallel)
        experiment_run = Convener(self.work_dir, experiment, n_experiments)
        experiment_run.go()

        df = pd.read_csv(experiment_run.data_file)

        self.assertEqual(df.shape[0], n_experiments*n_parallel)

        for ex_id, ex_df in df.groupby(df.ExperimentId):
            self.assertEqual(ex_df.shape[0], n_parallel)
            param_vals = ex_df.Arg0.tolist()
            self.assertTrue(all(p == param_vals[0] for p in param_vals[1:]))
            self.assertTrue(all(e == ex_id for e in ex_df.ExperimentId))
            self.assertTrue(all(n == n_parallel for n in ex_df.NParallel))

        self.assertEqual(experiment.n_parallel, 5)
        self.assertEqual(experiment.name, 'concurrent')
        self.assertEqual(experiment.quiet, False)
        self.assertEqual(experiment.seed, 1989 + n_experiments)
        self.assertEqual(experiment.ranges, ([1, 10], ))

        self.assertEqual(experiment_run.work_dir, self.work_dir)
        self.assertFalse(df.Errored.any())
