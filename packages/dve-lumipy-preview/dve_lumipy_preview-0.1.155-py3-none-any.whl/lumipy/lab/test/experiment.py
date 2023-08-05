import datetime as dt
import sys
import traceback
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Tuple, Union, List

import numpy as np
import pandas as pd

from lumipy.common.string_utils import indent_str
from lumipy.query.expression.table_op.base_table_op import BaseTableExpression


class Experiment:
    """The experiment class encapsulates an experiment on your luminesce. It is responsible for generating test query
    arguments, running a query from them, observing the behaviour and reporting the result back.

    """

    def __init__(self, name: str, build_fn: Callable, *ranges: Union[int, Tuple, List], **kwargs):
        """The constructor for the experiment class

        Args:
            name (str): name that labels the experiment.
            build_fn (Callable): a function that produces a query to run given some values.
            *ranges (Union[int, Tuple, List]): a single integer value to fix or a tuple range to uniformly sample for
            every argument to the build_fn.

        kwargs:
            quiet (bool):
            seed (int):
            n_parallel (int):
        """

        self.name = name
        self.build_fn = build_fn
        self.ranges = ranges

        self.quiet = kwargs.get('quiet', False)
        self.seed = kwargs.get('seed', np.random.randint(1989))
        self.n_parallel = kwargs.get('n_parallel', 1)

    def _build_experiment(self) -> Tuple[List[Union[int, float]], BaseTableExpression]:

        # Set the random seed each time so when this is called multiple times in the concurrent case the
        # randomly-generated parameters are the same.
        # This seed is then incremented when the entire run of concurrent jobs finishes.

        np.random.seed(self.seed)
        args = []
        for rng in self.ranges:
            if isinstance(rng, (int, float)):
                args.append(rng)
            else:
                # todo: distinguish between int and float here
                args.append(int(np.random.randint(rng[0], rng[1] + 1)))

        return args, self.build_fn(*args)

    def _job(self, quiet=False) -> pd.DataFrame:
        """A unit of work in the experiment. Allows for multiple to be run concurrently in different threads.

        This will run a single query to luminesce, monitor it and get the result. It will also log information about
        this process including any errors that may occur.

        Args:
            quiet (bool): whether printout feedback from the query should be suppressed

        Returns:
            DataFrame: the result of the observation
        """

        args, qry = self._build_experiment()

        if not quiet:
            print(indent_str(qry.get_sql(), 4), end='\n\n')
            print(f'    (Experiment values={args})', end='\n\n')

        start = dt.datetime.utcnow()
        job = None

        try:
            job = qry.go_async()
            submitted = dt.datetime.utcnow()
            job.interactive_monitor(quiet)
            get = dt.datetime.utcnow()
            df = job.get_result(quiet=quiet)
            end = dt.datetime.utcnow()
            row = {
                'ExecutionId': job.ex_id,
                'Start': start,
                'Submitted': submitted,
                'Get': get,
                'End': end,
                'ObsRows': df.shape[0],
                'ObsCols': df.shape[1],
                'Errored': False,
                'ErrorMessage': None
            }
        except Exception as e:
            end = dt.datetime.utcnow()
            exc_info = sys.exc_info()
            row = {
                'ExecutionId': job.ex_id if job is not None else None,
                'Start': start,
                'Submitted': pd.NaT,
                'Get': pd.NaT,
                'End': end,
                'ObsRows': None,
                'ObsCols': None,
                'Errored': True,
                'ErrorMessage': ''.join(traceback.format_exception(*exc_info)),
            }

        for i, a in enumerate(args):
            row[f'Arg{i}'] = a

        row['ExperimentName'] = self.name
        row['QueryTime'] = (row['Get'] - row['Start']).total_seconds()
        row['DownloadTime'] = (row['End'] - row['Get']).total_seconds()

        return pd.DataFrame([row])

    def observe(self) -> pd.DataFrame:
        """Run the experiment and log the results

        Returns:
            DataFrame: result of the experiment. This will have a row for each job.
        """

        dfs = []

        if isinstance(self.n_parallel, int):
            n_parallel = self.n_parallel
        else:
            np.random.seed((dt.datetime.utcnow() - dt.datetime(1970, 1, 2)).seconds)
            n_parallel = np.random.randint(self.n_parallel[0], self.n_parallel[1] + 1)

        with ThreadPoolExecutor(max_workers=n_parallel) as executor:

            tasks = [lambda: self._job(quiet=self.quiet)]
            tasks += [lambda: self._job(quiet=True)]*(n_parallel-1)

            if n_parallel > 1:
                print(f'    Running {n_parallel} concurrent queries')
                print(f'    Only showing a log for the first one.', end='\n\n')

            running = [executor.submit(t) for t in tasks]
            for r in running:
                dfs.append(r.result())

        self.seed += 1

        rdf = pd.concat(dfs)
        rdf['NParallel'] = n_parallel

        return rdf
