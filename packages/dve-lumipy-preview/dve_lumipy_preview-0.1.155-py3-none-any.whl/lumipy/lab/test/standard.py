from lumipy.atlas.base.base_provider_factory import BaseProviderFactory
from lumipy.lab import Experiment, Convener
from lumipy.query.expression.table.base_source_table import SourceTable
from typing import Tuple


def write_experiment(
        work_dir: str,
        writer: BaseProviderFactory,
        to_write: SourceTable,
        x_min=1,
        x_max=10000,
        n=50,
        concurrency=1,
):
    """A collection of experiments for writers measures writer performance with a data source that's held constant, and
    also measures the distribution of times for that constant data source.

    Args:
        work_dir (str): working directory to write data to.
        writer (BaseProviderFactory): the writer to use such as atlas.lusid_portfolio (note: use the atlas attribute, not
        the object initialised from it by calling atlas.lusid_portfolio()
        to_write (SourceTable): the data source to read data for the write test from.
        x_min (int): the upper limit of the range to sample the number of rows to write in the test.
        x_max (int): the upper limit of the range to sample the number of rows to write in the test.
        n (int): the number of times to run the experiment.
        concurrency (int): the number of simultaneous write queries to run.

    Returns:
        Tuple[str]: a pair of strings where the first is the baseline experiments result csv path and the second is the
        writer experiments result csv path.

    """

    def build(x):
        tv = to_write.select('*').limit(x).to_table_var()
        qry = writer(to_write=tv)
        return qry.select('*')

    writer_exp = Experiment(writer.get_name(), build, [x_min, x_max])
    writer_convener = Convener(work_dir, writer_exp, n)
    writer_convener.go()

    def baseline_build(x):
        # x doesn't so anything here, so we can plot it against the variable used above...
        return to_write.select('*')

    baseline_exp = Experiment(writer.get_name() + '_baseline', baseline_build, [x_min, x_max], n_parallel=concurrency)
    baseline_convener = Convener(work_dir, baseline_exp, n)
    baseline_convener.go()

    return baseline_convener.data_file, writer_convener.data_file
