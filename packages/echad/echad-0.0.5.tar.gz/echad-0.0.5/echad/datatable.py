from typing import MutableSequence, Optional, Sequence

from domonic.html import *

from . import consts
from .core import HTMLComponent


class DataTable(HTMLComponent):
    table_class = "w-full table-auto border-collapse border border-slate-400"
    td_class = "border border-slate-300 px-3 py-1"

    @staticmethod
    def make_group(offset: int, lst: Sequence, count=1):

        res = {}
        for i in range(0, len(lst), offset):
            val = lst[i : i + offset]
            res[count] = val
            count += 1

        return res

    def __init__(
        self,
        _id: str,
        rows: MutableSequence,
        offset: int = 40,
        _class: Optional[str] = None,
        *args,
        **kwargs,
    ) -> None:
        self._data = rows
        self._id = _id
        self.offset = offset
        super().__init__(*args, **kwargs)

    @property
    def json_data(self):
        return self._json_data_gen() if self._data else consts.EMPTY_NODE

    def _json_data_gen(self):
        import json

        d = self.make_group(self.offset, self._data)
        json_text = json.dumps(d)
        # json_text = json.dumps(self._data)

        CODE = json_text

        return script(
            CODE,
            _type=consts.JSON_TYPE,
            _id=f"data-{self._id}",
        )

    def build(self):

        first_page = self.make_group(self.offset, self._data)[1]
        hx_attrs = {
            "_hx-ext": "echad-table",
        }
        content = table(_id=self._id, _class=self.table_class, **hx_attrs).html(
            *[
                tr(
                    *[td(_class=self.td_class).html(info) for info in row],
                )
                # for row in self._data
                for row in first_page
            ],
        )

        # content = div(_id=self._id, **hx_attrs)
        return content
