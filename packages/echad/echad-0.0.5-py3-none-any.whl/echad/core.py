from typing import Dict, List, Optional, Tuple, Union

import pydash as _py
from bottle import Bottle, HTTPResponse, request, static_file
from domonic.html import *

from . import consts

############################## | Exceptions | ##############################


class EmptyBuilderError(Exception):
    def __init__(self) -> None:
        super().__init__("The build method must return nodes")


class OptionFieldError(Exception):
    def __init__(self, p) -> None:
        super().__init__(f"Can't get anything by path {p}")


############################## | Render utils | ##############################


def _open_browser(html: str):
    import tempfile
    import webbrowser
    from path import Path

    tmp = tempfile.NamedTemporaryFile(delete=True)
    path = Path(tmp.name + ".html")
    with open(path, "w") as f:
        f.write(html)
    webbrowser.open(f"file://{path}")
    return


def _assets_path(path: str):
    import os

    assets_base_path = os.environ.get("DASH_REQUESTS_PATHNAME_PREFIX") or "/"
    full_assets_path = assets_base_path + path
    return full_assets_path


def _dump_server(html: str):

    import os

    # assets_base_path = os.environ.get("DASH_REQUESTS_PATHNAME_PREFIX") or "/"
    # full_assets_path = assets_base_path + "assets/<f:path>"
    # Only works on YOUDAO Server
    host = "0.0.0.0" if os.environ.get("DASH_REQUESTS_PATHNAME_PREFIX") else "127.0.0.1"
    serv = Bottle()
    folder = consts.LOCAL.ASSETS

    serv.route(
        "/assets/<f:path>",
        callback=lambda f: static_file(f, root=folder),
    )
    serv.route("/", callback=lambda: HTTPResponse(html, status=200))
    serv.run(host=host, port=8050)
    return


############################## | HTMLComponent | ##############################
class HTMLComponent(HTMLElement):
    # class HTMLComponent(Node):
    name = "chadcpt"

    def build(self):
        return NotImplementedError

    def __str__(self):
        res = self.build()
        # if not res:
        #     raise EmptyBuilderError
        # assert isinstance(res, HTMLElement)
        assert isinstance(res, Node)
        res >> self.kwargs
        return str(res)

    def render(self, server=False):
        if server:
            page = ChadPage(
                self,
                echarts_src=_assets_path("assets/echarts.min.js"),
                htmx_src=_assets_path("assets/htmx.min.js"),
                chadext_src=_assets_path("assets/charty.js"),
                tailwind_src=_assets_path("assets/tailwind.min.css"),
            )
            return _dump_server(str(page))
        page = ChadPage(self)
        _open_browser(str(page))
        return


############################## | ChartMixin | ##############################
"""
{
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
"""


class ChartMixin:
    _data: Dict
    _series_data_path = "series.0.data"
    _series_path = "series"
    _legend_path = "legend"
    _tooltip_path = "legend"

    @property
    def data(self) -> List:
        if not _py.has(self._data, self._series_data_path):
            raise OptionFieldError(self._series_data_path)

        return _py.get(self._data, self._series_data_path)

    @property
    def legend(self):
        if not _py.has(self._data, self._legend_path):
            raise OptionFieldError(self._legend_path)

        return _py.get(self._data, self._legend_path)

    @property
    def series(self):
        if not _py.has(self._data, self._series_path):
            raise OptionFieldError(self._series_path)

        return _py.get(self._data, self._series_path)

    @property
    def tooltip(self):
        if not _py.has(self._data, self._tooltip_path):
            raise OptionFieldError(self._tooltip_path)

        return _py.get(self._data, self._tooltip_path)

    def set(self):
        return NotImplementedError

    def add(self, *args, **kwd):

        """
        E.g
        add(name="hello",value=12) -> {"name":"hello", "value":12}\n
        then append it into series.data

        if to pass a list for barchart please use the "d" e.g
        add(d=[1,2,3,4])


        """
        if kwd and args:
            raise Exception
        if kwd:
            self.data.append(kwd)
        if args:
            for i in args:
                self.data.append(i)
        return self


############################## | BaseChart | ##############################


class BaseChart(HTMLComponent):
    OPTION: Optional[Dict] = None
    CSS: Optional[Dict] = None

    def __init__(
        self,
        _id: str,
        url: str = "",
        data: Dict = {},
        theme: str = "light",
        *args,
        **kwargs,
    ):
        _style = kwargs.get("style")
        if not _style:
            kwargs["style"] = "height:500px;width:100%;"
        if _style and "height" not in _style:
            kwargs["style"] += ";height:500px;width:100%;"

        self._id = _id
        self.url = url
        self.theme = theme
        # self._data = data
        self._data = self.OPTION or data
        self.args = args
        super().__init__(*args, **kwargs)

    @property
    def json_data(self):
        return self._json_data_gen() if self._data else consts.EMPTY_NODE

    def _json_data_gen(self):
        import json

        json_text = json.dumps(self._data)

        CODE = json_text

        return script(
            CODE,
            _type=consts.JSON_TYPE,
            _id=f"data-{self._id}",
        )

    def build(self, **kwd):

        hx_attrs = {
            "_hx-ext": "echad",
            "_hx-swap": "none",
        }
        if self.url:
            hx_attrs["_hx-get"] = self.url
            hx_attrs["_hx-trigger"] = "load"

        content = div(
            _id=self._id,
            _theme=self.theme,
            **self.kwargs,
            **hx_attrs,
        ).html(*self.args)
        return content


############################## | ChadPage | ##############################


class ChadPage:
    CSS = """
    body{
        background-color: #0F0D28;
    }


    """

    def __init__(
        self,
        *args,
        js: List[str] = [],
        css: List[str] = [],
        echarts_src: Optional[str] = None,
        chadext_src: Optional[str] = None,
        htmx_src: Optional[str] = None,
        tailwind_src: str = consts.LOCAL.TAILWIND,
        dark_mode=False,
        **kwd,
    ):
        self._js = js
        self._css = css
        self._htmx_src = htmx_src
        self._echarts_src = echarts_src
        self._chad_ext_src = chadext_src
        self._tailwind_src = tailwind_src
        self._dark_mode = dark_mode
        self.args = args
        self.kwd = kwd

    def _load_json_chart_option(self, children: Union[List, Tuple]):
        script_list = []
        # for child in children:
        #     if hasattr(child, "json_data"):
        #         data = child.json_data
        #         if data:
        #             script_list.append(data)

        for child in children:
            res = child.querySelectorAll("chadcpt")
            if res:
                # data = child.json_data
                return [e.json_data for e in res]

        return script_list

    def __str__(self):
        tailwind = (
            link(_rel=consts.REL, _href=self._tailwind_src)
            if self._tailwind_src
            else consts.EMPTY_NODE
        )

        js_list = (
            [script(_type=consts.JS_TYPE, _src=j) for j in self._js]
            if self._js
            else consts.EMPTY_NODE
        )

        css_list = (
            [link(_rel=consts.REL, _href=c) for c in self._css]
            if self._css
            else consts.EMPTY_NODE
        )

        htmx_src = (
            script(_type=consts.JS_TYPE, _src=self._htmx_src)
            if self._htmx_src
            else script(_type=consts.JS_TYPE, _src=consts.LOCAL.HTMX)
            # else script(_type=consts.JS_TYPE, _src=consts.CDN.HTMX)
        )
        echart_src = (
            script(_type=consts.JS_TYPE, _src=self._echarts_src)
            if self._echarts_src
            # else script(_type=consts.JS_TYPE, _src=consts.CDN.ECHARTS)
            else script(_type=consts.JS_TYPE, _src=consts.LOCAL.ECHARTS)
        )
        chad_ext = (
            script(_type=consts.JS_TYPE, _src=self._chad_ext_src)
            if self._chad_ext_src
            # else script(consts.ECHAD_EXT, _type=consts.JS_TYPE)
            else script(_src=consts.LOCAL.ECHAD_EXT, _type=consts.JS_TYPE)
        )

        _json_data_scripts = self._load_json_chart_option(self.args)
        mode = style(self.CSS) if self._dark_mode else ""
        content = html(
            head(
                tailwind,
                mode,
                htmx_src,
                echart_src,
                chad_ext,
                *js_list,
                *css_list,
            ),
            body(*self.args, *_json_data_scripts, **self.kwd),
        )

        return str(content)

    def render(self, server=False):
        if server:

            self._echarts_src = _assets_path("assets/echarts.min.js")
            self._htmx_src = _assets_path("assets/htmx.min.js")
            self._chad_ext_src = _assets_path("assets/charty.js")
            self._tailwind_src = _assets_path("assets/tailwind.min.css")

            return _dump_server(str(self))
        _open_browser(str(self))
        return
