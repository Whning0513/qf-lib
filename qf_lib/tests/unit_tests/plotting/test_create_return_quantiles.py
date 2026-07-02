import unittest
from datetime import datetime

import pandas as pd

from qf_lib.containers.series.simple_returns_series import SimpleReturnsSeries
from qf_lib.plotting.charts.boxplot_chart import BoxplotChart
from qf_lib.plotting.helpers.create_return_quantiles import create_return_quantiles


class TestCreateReturnQuantiles(unittest.TestCase):
    def test_live_date_chart_uses_hue_for_is_oos_groups(self):
        returns = SimpleReturnsSeries(
            data=[0.01, 0.02, -0.01, 0.03],
            index=pd.to_datetime(["2020-01-01", "2020-01-02", "2020-01-08", "2020-02-05"]),
        )

        chart = create_return_quantiles(returns, live_start_date=datetime(2020, 1, 8))

        self.assertIsInstance(chart, BoxplotChart)
        self.assertEqual("frequency", chart.plot_settings["x"])
        self.assertEqual("returns", chart.plot_settings["y"])
        self.assertEqual("sample", chart.plot_settings["hue"])
        self.assertIsInstance(chart._data, pd.DataFrame)
        self.assertEqual({"returns", "frequency", "sample"}, set(chart._data.columns))
        self.assertEqual({"IS", "OOS"}, set(chart._data["sample"]))
        self.assertEqual({"daily", "weekly", "monthly"}, set(chart._data["frequency"]))


if __name__ == "__main__":
    unittest.main()
