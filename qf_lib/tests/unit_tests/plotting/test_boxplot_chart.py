import unittest
from unittest.mock import patch

import matplotlib
import pandas as pd
matplotlib.use("Agg")

import matplotlib.pyplot as plt

from qf_lib.plotting.charts.boxplot_chart import BoxplotChart


class TestBoxplotChart(unittest.TestCase):
    @patch("qf_lib.plotting.charts.boxplot_chart.sns.boxplot")
    def test_plot_does_not_pass_palette_without_hue(self, boxplot_mock):
        chart = BoxplotChart([pd.Series([1.0, 2.0]), pd.Series([3.0, 4.0])], linewidth=1)

        chart.plot()

        _, kwargs = boxplot_mock.call_args
        self.assertNotIn("palette", kwargs)
        self.assertIsInstance(kwargs["data"], pd.DataFrame)
        self.assertEqual(1, kwargs["linewidth"])
        plt.close(chart.figure)

    @patch("qf_lib.plotting.charts.boxplot_chart.sns.boxplot")
    def test_plot_keeps_palette_when_hue_is_provided(self, boxplot_mock):
        palette = ["#112233", "#445566"]
        chart = BoxplotChart(
            pd.DataFrame({"value": [1.0, 2.0], "group": ["a", "b"]}),
            linewidth=1,
            hue="group",
            palette=palette,
        )

        chart.plot()

        _, kwargs = boxplot_mock.call_args
        self.assertEqual(palette, kwargs["palette"])
        self.assertEqual("group", kwargs["hue"])
        plt.close(chart.figure)

    def test_plot_accepts_list_of_series_with_real_seaborn(self):
        chart = BoxplotChart([pd.Series([1.0, 2.0]), pd.Series([3.0, 4.0])], linewidth=1)

        chart.plot()

        self.assertIsNotNone(chart.axes)
        plt.close(chart.figure)


if __name__ == "__main__":
    unittest.main()
