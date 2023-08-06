"""
blink/core/resource.py
Ian Kollipara
2022.03.31

API Resource Decorator
"""

# Imports
from dataclasses import dataclass
from inspect import getmembers, isfunction
from typing import Generic, List, Optional, Type, TypeVar

from falcon import Request, Response

from .base_decorator import BaseDecorator, Dependency
from .protocols.resource import ResourceT

# Generic Type Variable

_T = TypeVar("_T")


@dataclass(frozen=True)
class ResourceType(Generic[_T]):
    """ResourceType represents what the @Resource
    decorator returns.

    | Attributes | Type | Description               |
    |------------|------|---------------------------|
    | route      | str  | the api route             |
    | obj        | T    | The resource class object |
    """

    route: str
    obj: _T


class Resource(BaseDecorator):
    """Resource Decorator

    Each API falcon resource should be decorated with
    `@Resource` above it. This allows the user to set the
    path and path parameters for the route as well.

    Example:
    ```python
    @Resource("/test", [{"dependency": SomeClass}])
    class Test:
       def __init__(self, some_class: SomeClass) -> None:
           self.some_class = some_class
           ...
    ```
    """

    def __init__(
        self, route: str, dependencies: Optional[List[Dependency]] = None
    ) -> None:
        super().__init__(dependencies)
        self.dependencies = dependencies or []
        self.route = route

    def __call__(self, resource_cls: Type[ResourceT]) -> ResourceType[ResourceT]:

        # Given our methods return HTML, we need to wrap them in a way
        # that Falcon can handle, which means the res.text attribute
        # is set to the result of our method
        for method_name, method in filter(
            lambda method: method[0][:2] == "on", getmembers(resource_cls, isfunction)
        ):

            def _wrapper(base: ResourceT, req: Request, res: Response, *args):
                res.text = method(base, req, res, *args)

            setattr(resource_cls, method_name, _wrapper)

        # The main idea here is what happens when the
        # resource class is called, such as
        # Resource("/test")(Test)
        # Which is what happens with the decorator
        obj = (
            resource_cls(**self.initialize_dependencies())  # type: ignore
            if len(self.initialize_dependencies())
            else resource_cls()
        )
        return ResourceType(self.route, obj)
