#     Copyright 2016-present CERN – European Organization for Nuclear Research
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

from typing import List, Tuple, Union

import pandas as pd
import seaborn as sns

from qf_lib.containers.series.qf_series import QFSeries
from qf_lib.plotting.charts.chart import Chart


class BoxplotChart(Chart):
    """
    Creates a box plot consisting of the list of ``QFSeries`` specified in ``data``.

    Parameters
    ----------
    data: Union[List[QFSeries], pd.DataFrame]
       A list of ``QFSeries`` or a ``DataFrame`` in seaborn wide or long form.
    plot_settings
       Passed to Seaborn plotting function.
    """

    SERIES_KEY = "series"
    """Used for storing the boxplot chart's series."""

    def __init__(self, data: Union[List[QFSeries], pd.DataFrame], **plot_settings):
        super().__init__(start_x=None, end_x=None)
        self._data = data
        self.plot_settings = plot_settings

    def plot(self, figsize: Tuple[float, float] = None):
        self._setup_axes_if_necessary(figsize)

        plot_kwargs = dict(self.plot_settings)

        # Seaborn requires hue when a custom palette is supplied in recent versions.
        if "palette" in plot_kwargs:
            palette = plot_kwargs.pop("palette")
            sns.boxplot(ax=self.axes, data=self._data, palette=palette, **plot_kwargs)
        elif plot_kwargs.get("hue") is not None:
            colors = Chart.get_axes_colors()
            palette = sns.color_palette(colors, n_colors=len(colors))
            sns.boxplot(ax=self.axes, data=self._data, palette=palette, **plot_kwargs)
        else:
            sns.boxplot(ax=self.axes, data=self._data, **plot_kwargs)

        self._adjust_style()
        self._apply_decorators()
