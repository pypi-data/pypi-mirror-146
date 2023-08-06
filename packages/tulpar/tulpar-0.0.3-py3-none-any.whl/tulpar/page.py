"""
tulpar/page.py
Ian Kollipara
2022.04.04

Page Decorator Definition
"""

# Imports
from functools import partial
from typing import Type

from falcon import Request, Response

from .base_decorator import BaseDecorator
from .protocols.page import PageFunc


class Page(BaseDecorator):
    """Tulpar Page Decorator.

    This denotes what is a normal page in a Tulpar application.
    It allows for dependency injection just like a resource, but
    is handled differently behind the scenes. A page should be
    a function that has at least two parameters: req and res.

    Example:
    ```python
    @Page()
    def index(req, res):
        return HTML("<p>Hello World</p>")
    ```
    """

    def __call__(self, page_func: PageFunc) -> Type:
        cls_name = "".join(map(str.capitalize, page_func.__name__.split("_")))  # type: ignore
        page_with_deps = partial(page_func, **self.initialize_dependencies())

        # This function wraps your endpoint so that returning the
        # html actually renders it. The first argument is a _,
        # as that's the base object being passed in. However,
        # there's no need for a base object, as its just a
        # wrapped function.
        def _register_on_get(_, req: Request, res: Response):
            res.text = page_with_deps(req, res)

        cls = type(cls_name, (), {"on_get": _register_on_get})
        return cls
