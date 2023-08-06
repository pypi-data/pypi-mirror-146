from typing import Callable, Dict, List, Optional, Tuple, Union
from abc import ABCMeta, abstractmethod
from domonic.html import Element
from domonic.html import *
from . import consts


def _render(cpnt, include_tailwind=True):
    import tempfile
    import webbrowser
    from path import Path

    tailwind = []
    if include_tailwind:
        tailwind.append(consts.LOCAL.TAILWIND)

    page = ChadPage(css=tailwind).html(cpnt)
    # tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp = tempfile.NamedTemporaryFile(delete=True)
    path = Path(tmp.name + ".html")
    with open(path, "w") as f:
        f.write(str(page))
    webbrowser.open(f"file://{path}")
    return


def _render2(html: "HTMLComponent"):
    content = str(html.html())
    _open_browser(content)
    return


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


class Base(metaclass=ABCMeta):
    def __str__(self):
        if hasattr(self, "_html"):
            return str(self._html)
        return str(self.build())

    def html(self, *args):
        """
        Used for addtional DOM content eg. C(a=1,b=2).html(extra)
        when it has addtional DOM nodes, they should be declare to self._html
        If a Base instance doesn't have a _html attr, that means it has't call
        self.html() method also means it's a instance with only attrs

        """
        self._html = self.build(*args)
        return self._html

    @abstractmethod
    def build(self) -> Element:
        ...


class HTMLComponent(Base):
    renderer: Callable

    def render(self):
        return self.renderer(self)


class BaseChart(HTMLComponent):

    renderer = _render

    def __init__(
        self,
        _id: str,
        url: str = "",
        style: str = "",
        theme: str = "light",
        data: Dict = {},
        **kwd,
    ):
        self._id = _id
        self.url = url
        self._data = data
        self._theme = theme
        self._style = style
        self._kwd = kwd

        if not self._style:
            self._style = "height:500px"

        if self._style and "height" not in self._style:
            self._style += ";height:500px"

    # def render(self, include_tailwind=True):
    #     return _render(self, include_tailwind=True)

    def html(self, *args):
        if args:
            raise ValueError(
                "Shouldn't insert addtional nodes into an echart HTML block"
            )
        else:
            return super().html()

    def _json_data_gen(self):
        import json

        json_text = json.dumps(self._data)

        CODE = json_text

        return script(
            CODE,
            _type=consts.JSON_TYPE,
            _id=f"data-{self._id}",
        )

    @property
    def extra_option(self):

        return self._json_data_gen() if self._data else consts.EMPTY_NODE

    def build(self, *args) -> Element:

        hx_attrs = {
            "_hx-ext": "echad",
            "_hx-swap": "none",
        }
        if self.url:
            hx_attrs["_hx-get"] = self.url
            hx_attrs["_hx-trigger"] = "load"

        content = div(
            _id=self._id,
            _theme=self._theme,
            _style=self._style,
            **self._kwd,
            **hx_attrs,
        )

        return content


class ChadPage(HTMLComponent):
    renderer = _render2

    def __init__(
        self,
        js: List[str] = [],
        css: List[str] = [],
        echarts_src: Optional[str] = None,
        chadext_src: Optional[str] = None,
        htmx_src: Optional[str] = None,
    ):
        self._js = js
        self._css = css
        self._htmx_src = htmx_src
        self._echarts_src = echarts_src
        self.chad_ext_src = chadext_src

    def _load_static_chart_option(self, children: Union[List, Tuple]):
        res_list = []
        for child in children:
            # has to be a BaseChart or has attr extra_option
            # if isinstance(child, BaseChart):
            if hasattr(child, "extra_option"):
                extra_option = child.extra_option
                if extra_option:
                    res_list.append(extra_option)
                # assert isinstance(extra_option, script)

        return res_list

    def html(self, *args):
        extras = self._load_static_chart_option(args)
        total = [*args, *extras]
        self._html = self.build(*total)
        # or just return super().html(*total)

        return self._html

    def build(self, *children):

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
            script(_type=consts.JS_TYPE, _src=self.chad_ext_src)
            if self.chad_ext_src
            else script(consts.ECHAD_EXT, _type=consts.JS_TYPE)
        )
        content = html(
            head(
                htmx_src,
                echart_src,
                chad_ext,
                *js_list,
                *css_list,
            ),
            body(*children),
        )

        return content
