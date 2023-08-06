from typing import Dict, List, Union

import pydash as _

from .core import BaseChart, ChartMixin


"""
{
    "tooltip": {"trigger": "item"},
    "legend": {"top": "5%", "left": "center"},
    "series": [
        {
            "name": "Access From",
            "type": "pie",
            "radius": ["40%", "70%"],
            "avoidLabelOverlap": False,
            "itemStyle": {"borderRadius": 10, "borderColor": "#fff", "borderWidth": 2},
            "label": {"show": False, "position": "center"},
            "emphasis": {
                "label": {"show": True, "fontSize": "40", "fontWeight": "bold"}
            },
            "labelLine": {"show": False},
            "data": [
                {"value": 1048, "name": "Search Engine"},
                {"value": 735, "name": "Direct"},
                {"value": 580, "name": "Email"},
                {"value": 484, "name": "Union Ads"},
                {"value": 300, "name": "Video Ads"},
            ],
        }
    ],
}
"""


class PieChart(BaseChart, ChartMixin):
    OPTION = {
        "tooltip": {"trigger": "item"},
        "legend": {"top": "5%", "left": "center"},
        "series": [
            {
                "name": "",
                "type": "pie",
                # "radius": ["40%", "70%"],
                "avoidLabelOverlap": False,
                "itemStyle": {
                    "borderRadius": 10,
                    "borderColor": "#fff",
                    "borderWidth": 2,
                },
                "label": {"show": False, "position": "center"},
                "emphasis": {
                    "label": {"show": True, "fontSize": "30", "fontWeight": "bold"}
                },
                "labelLine": {"show": False},
                "data": [],
            }
        ],
    }


############################## | Deprecated | ##############################


# def add(self, *, name: str, value, **kwd):

#     d = _.get(self._data, self.data_path)
#     assert isinstance(d, List)
#     d.append({"name": name, "value": value, **kwd})
#     return self
