from typing import Dict, List

from domonic.html import *

from .core import HTMLComponent


class Dropdown(HTMLComponent):
    select_css = "rounded-md border px-3 py-1 font-thin hover:border-blue-400 hadow-sm"

    def __init__(self, _id: str, items: List[Dict], url: str = "", *args, **kwargs):
        self.items = items
        self._id = _id
        self.url = url

        super().__init__(*args, **kwargs)

    def build(self):
        hx_attrs = {"_hx-get": self.url, "_hx-target": ""}

        content = select(
            _id=self._id,
            _name=f"{self._id}-name",
            _class=self.select_css,
            **hx_attrs,
        ).html(
            *[option(_value=item["value"]).html(item["text"]) for item in self.items]
        )
        return form(content)
