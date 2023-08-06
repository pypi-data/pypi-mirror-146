from typing import Dict, Union

import pydash as _py

from .core import BaseChart, ChartMixin


############################## | Example Option | ##############################
# {
#     "tooltip": {"formatter": "{a} <br/>{b} : {c}%"},
#     "series": [
#         {
#             "name": "Pressure",
#             "type": "gauge",
#             "detail": {"formatter": "{value}"},
#             "data": [{"value": 25, "name": "SCORE"}],
#         },
#     ],
# }
############################## |   GaugeChart  | ##############################
class GaugeChart(BaseChart, ChartMixin):

    OPTION = {
        "tooltip": {"formatter": "{a} <br/>{b} : {c}%"},
        "legend": {},
        "series": [
            {
                "name": "",
                "type": "gauge",
                "detail": {"formatter": "{value}"},
                "data": [],
            }
        ],
    }


class MultiGaugeChart(BaseChart):

    ...


############################## | Deprecated | ##############################
# def add(self, *, name: str, value: Union[int, float], **kwd):
#     # stupid as fuck
#     # data = {"value": None, "name": None}
#     # data["value"] = value
#     # data["name"] = name
#     # self._data["series"][0]["data"].append(data)
#     data = {"value": value, "name": name}
#     _py.set_(self._data, "series.0.data.0", data)

#     return self

# def set_series(self, d: Dict):
#     # self._data["series"][0] = d
#     _py.set_(self._data, "series.0", d)
#     return self

# def set_tooltip(self, d: Dict):
#     _py.set_(self._data, "tooltip", d)
#     return self
