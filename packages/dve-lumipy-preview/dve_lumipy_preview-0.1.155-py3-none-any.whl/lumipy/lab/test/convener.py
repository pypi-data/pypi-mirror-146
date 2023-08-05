import datetime as dt
import os
import time
from pathlib import Path

import numpy as np
from IPython.display import clear_output
import uuid
from lumipy.common.string_utils import indent_str


class Convener:
    """ The convener looks after your data-taking run and reports back useful information about run times, errors
    and an estimate of when the experimental run will finish. It writes the results of its observations as it goes.
    The data taking run is a series of observations of the given experiment.

    """

    def __init__(self, work_dir: str, experiment: 'Experiment', n_obs: int, err_wait: int = 15):
        """Constructor for the convener class.

        Args:
            work_dir (str): the working directory to write results to.
            experiment (Experiment): the experiment to run.
            n_obs (int): the number of observations (number of times to run the experiment).
            err_wait (int): the amount of time to pause after getting an error during an observation.
        """

        self.work_dir = work_dir
        self.experiment = experiment
        self.n_experiments = n_obs
        self.err_wait = err_wait

        data_dir = f'{self.work_dir}/data'
        Path(data_dir).mkdir(parents=True, exist_ok=True)
        Path(f'{self.work_dir}/plots').mkdir(parents=True, exist_ok=True)

        self.data_file = f'{data_dir}/{self.experiment.name}.csv'

    def go(self) -> None:
        """Begin the data-taking

        """

        error_count = 0
        run_start = dt.datetime.utcnow()
        offset = dt.datetime.now() - dt.datetime.utcnow()

        # Very important.
        emoji = np.random.choice(['🧪', '🔭', '⚗️', '🧬', '🔬'])

        clear_output(wait=True)

        times = []
        start = None
        for i in range(1, self.n_experiments + 1):

            print(f"Doing Science! {emoji}")
            print(f"  Experiment name: {self.experiment.name}")
            print(f"  Run started at: {(run_start + offset).strftime('%Y-%m-%d %H:%M:%S')}")

            new_start = dt.datetime.utcnow()
            if start is not None:
                times.append((new_start - start).total_seconds())
            start = new_start

            if len(times) > 1:
                t_mean = np.mean(times)
                t_sum = np.sum(times)
                t_std_err = np.std(times)/(len(times) - 1)
                est_len = self.n_experiments * t_mean / 60
                est_finish = run_start + dt.timedelta(minutes=est_len) + offset
                print(f"    Mean experiment time: {t_mean:2.2f}s ±{t_std_err:2.2}s")
                print(f"    Total experiment time so far: {t_sum:2.2f}s")
                print(f"    Estimated total experiment time: {est_len:2.2f}min → finish @ {est_finish.strftime('%H:%M:%S')}")

            if len(times) > 0:
                print(f"    Error count: {error_count}")

            print(f"    Experiment {i}/{self.n_experiments} started at {(start + offset).strftime('%H:%M:%S')}\n")

            res = self.experiment.observe()
            res['RunStart'] = run_start
            res['ExperimentId'] = str(uuid.uuid4())

            print(f'Appending to {self.data_file}')
            res.to_csv(self.data_file, index=False, mode='a', header=not os.path.exists(self.data_file))

            if any(res['Errored'].tolist()):
                error_count += 1
                print(f"Waiting {self.err_wait}s after getting an error...")
                err_msg = indent_str('\n'.join(e for e in res['ErrorMessage'] if e is not None), 4)
                print(f"Error:\n{err_msg}")
                time.sleep(self.err_wait)

            clear_output(wait=True)
