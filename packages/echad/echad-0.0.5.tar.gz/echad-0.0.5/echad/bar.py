from typing import List

import pydash as _

from .core import BaseChart, ChartMixin


"""
OPTION = {
    "xAxis": {
        "type": "category",
        "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    },
    "yAxis": {"type": "value"},
    "series": [
        {
            "data": [120, 200, 150, 80, 70, 110, 130],
            "type": "bar",
            "showBackground": True,
            "backgroundStyle": {"color": "rgba(180, 180, 180, 0.2)"},
        }
    ],
}
"""


class BarChart(BaseChart, ChartMixin):
    OPTION = {
        "xAxis": {
            "type": "category",
            "data": [],
        },
        "yAxis": {"type": "value"},
        "series": [
            {
                "data": [],
                "type": "bar",
                "showBackground": True,
                "backgroundStyle": {"color": "rgba(180, 180, 180, 0.2)"},
            }
        ],
    }

    def add_xaxis(self, *args):
        y = _.get(self._data, "xAxis.data")
        assert isinstance(y, List)
        y += args
        return self

    def add_yaxis(self, *args):
        return self.add(*args)
