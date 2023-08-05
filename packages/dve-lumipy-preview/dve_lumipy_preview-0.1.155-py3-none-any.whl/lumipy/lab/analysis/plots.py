import numpy as np
import pandas as pd

from lumipy.lab.analysis.models import QuantileFits

_cms_scheme = {
    'scatter_plot': {'color': 'black', 'alpha': 2 / 3},
    'median_line': {'color': 'black', 'ls': '-'},
    'outer_band': {'color': 'lime', 'alpha': 1.0},
    'inner_band': {'color': 'yellow', 'alpha': 1.0},
}


def _make_monochrome_scheme(c):
    return {
        'scatter_plot': {'color': c, 'alpha': 2 / 3},
        'median_line': {'color': c, 'ls': '-'},
        'outer_band': {'color': c, 'alpha': 1 / 6},
        'inner_band': {'color': c, 'alpha': 1 / 3},
    }


def band_plot(ax, df: pd.DataFrame, model: QuantileFits, label: str, color_scheme: str = 'cms'):
    """Produce the standard quantile band plot

    Args:
        ax: the matplotlib axes to draw on
        df (DataFrame): the pandas dataframe containing the data to use.
        model (QuantileFits): the quantile fits instance containing the fitted quantile regressions.
        label (str): label to attach to legend entries to distinguish this series.
        color_scheme (str): color scheme to use. Values can be any valid matplotlib color, or 'cms' for a CMS-style
        Brazil band plot.

    """

    if color_scheme == 'cms':
        scheme = _cms_scheme
    else:
        scheme = _make_monochrome_scheme(color_scheme)

    x_min = df[model.x].min()
    x_max = df[model.x].max()

    x = np.linspace(x_min, x_max, 3)
    ax.scatter(df[model.x], df[model.y], s=10, zorder=99, label=f'Obs ({label})', **scheme['scatter_plot'])

    cp05, mp05 = model.get_params(0.05)
    cp25, mp25 = model.get_params(0.25)
    cp50, mp50 = model.get_params(0.50)
    cp75, mp75 = model.get_params(0.75)
    cp95, mp95 = model.get_params(0.95)

    p05 = x * mp05 + cp05
    p25 = x * mp25 + cp25
    p50 = x * mp50 + cp50
    p75 = x * mp75 + cp75
    p95 = x * mp95 + cp95

    ax.plot(x, p50, label=f'Median ({label})', **scheme['median_line'])
    ax.fill_between(x, p25, p75, label=f'p25-p75 Range ({label})', **scheme['inner_band'])
    ax.fill_between(x, p75, p95, label=f'p5-p95 Range ({label})', **scheme['outer_band'])
    ax.fill_between(x, p05, p25, **scheme['outer_band'])

    ax.set_ylabel('Query Time (s)')
    ax.grid(True, ls=':', zorder=-99)
    ax.legend(fontsize=12, loc=2)
