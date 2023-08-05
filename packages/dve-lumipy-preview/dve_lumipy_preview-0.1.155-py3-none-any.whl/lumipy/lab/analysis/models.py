from typing import List, Optional
import pandas as pd
import statsmodels.api as sm
from statsmodels.regression.quantile_regression import QuantReg


class QuantileFits:
    """Class that encapsulates a collection of quantile regressions applied to luminesce performance data

    """

    def __init__(
            self,
            data: pd.DataFrame,
            x: str, y: str,
            quantiles: Optional[List[float]] = None
    ):
        """Constructor for the QuantileFits class

        Args:
            data (DataFrame): the data to use
            x (str): the column name of the independent variable
            y (str): the column name of the dependent variable
            quantiles (Optional[List[float]]): quantiless to compute linear quantile regression fits for.
        """

        if quantiles is None:
            quantiles = [0.05, 0.25, 0.5, 0.75, 0.95]

        self.x = x
        self.y = y

        model = QuantReg(
            data[self.y],
            sm.add_constant(data[self.x])
        )

        self.fits = {q: model.fit(q) for q in quantiles}

    def get_result(self, q: float):
        """Get the result object of a given quantile in the fits.

        Args:
            q (float): quantile to get the result for.

        Returns:
            The statsmodels fit result object
        """
        return self.fits[q]

    def get_params(self, q: float):
        """Get the parameters of the line corresponding to the given quantile.

        Args:
            q (float): the quantile to get the line parameters for.

        Returns:
            List[float]: pair of values consisting of the intercept and gradient of the line.
        """
        res = self.get_result(q)
        return res.params.tolist()
