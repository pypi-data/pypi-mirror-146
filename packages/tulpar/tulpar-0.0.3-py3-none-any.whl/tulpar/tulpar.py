"""
blink/blink.py
Ian Kollipara
2022.03.31

Tulpar Application Class Definition
"""

# Imports
from importlib import import_module
from os import chdir, getcwd, listdir
from os.path import isdir
from typing import Generator, final

from falcon import App
from jinja2 import Environment, PackageLoader, select_autoescape
from pony.orm import Database

from .config import TulparConfig
from .protocols.resource import HTML
from .resource import ResourceType


def get_all_files_in(directory: str) -> Generator[str, None, None]:
    """Get all files in the given directory, recursively.

    Get all the files in a given directory, including subdomains.
    """

    for file in filter(lambda file: file[0] != "_", listdir(directory)):
        if isdir(f"{directory}/{file}"):
            yield from get_all_files_in(f"{directory}/{file}")
        else:
            yield file


@final
class Tulpar:
    """Tulpar

    Tulpar is the main application class of Tulpar Programs.
    It includes the registration of pages, the registration of api routes,
    the configuration of the database, the creation of the tempalate engine,
    among other things as well.

    It is not to be subclassed, but middleware may be given as a list of
    parameters.
    """

    __app_dir = getcwd().split("/")[-1].replace("-", "_").lower()
    config: TulparConfig = import_module(f"{__app_dir}.config").config()
    db = Database()
    template_env = Environment(
        loader=PackageLoader(__app_dir), autoescape=select_autoescape(("html"))
    )
    __app = App("text/html; charset=utf-8", middleware=config.middleware)

    def __init__(self) -> None:
        chdir(self.__app_dir)
        Tulpar.db.bind(provider=self.config.db_params[0], **self.config.db_params[1])
        Tulpar.db.generate_mapping(create_tables=True)
        self.register_page_directory("pages")
        self.register_api_directory("resources")

    def __call__(self, env, start_response) -> App:
        return self.__app(env, start_response)

    def register_page_directory(self, directory: str) -> None:
        """Register the directory contents as a page.

        Given a real directory, register the module classes as pages to the given
        application. Recurse down the directory tree, building a route prefix value
        with each recursive descent.

        This skips all files that begin with an underscore(_). This includes directories.
        """

        for mod in get_all_files_in(directory):

            mod_path = mod.replace("/", ".")[:-3]
            mod_route = "/".join(mod.split("/")[1:])
            mod_cls = mod_path.split(".")[-1]

            page = getattr(import_module(f"{self.__app_dir}.{mod_path}"), mod_cls)()

            if mod_cls == "index":
                mod_route = "/".join(mod_route.split("/")[:-1])
                self.__app.add_route(f"/{mod_route}", page)
            else:
                self.__app.add_route(f"/{mod_route[:-3]}", page)

    def register_api_directory(self, directory: str):
        """Register the directory as an api route.

        Given a valid directory, recursively add all the files as api routes. This
        is determined by classes denoted with @Resource Decorator. This also
        shows the path.

        In this case the route prefix adjusts for nested areas. Just like page
        variation, this skips all files that begin with an underscore(_), including
        directories.
        """

        for resource in get_all_files_in(directory):

            mod = resource.replace("/", ".")[:-3]
            rcls = "".join(map(str.capitalize, resource.split("/")[-1][:-3].split("_")))

            resource_type: ResourceType = getattr(import_module(f"{self.__app_dir}.{mod}"), rcls)

            self.__app.add_route(resource_type.route, resource_type.obj)


def render(template_name: str, **kwargs) -> HTML:
    """render the given template using the given args.

    Given a valid template address (which is assumed to be within "templates")
    render the given template with the extra args, passed as keyword args.
    """

    return HTML(Tulpar.template_env.get_template(template_name).render(kwargs))
