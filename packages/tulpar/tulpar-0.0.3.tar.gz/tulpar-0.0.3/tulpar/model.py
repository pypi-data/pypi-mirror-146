"""
tulpar/model.py
Ian Kollipara
2022.04.10

Model Decorator Definition
"""

# Imports
from typing import Type

from .tulpar import Tulpar


class Model:
    """Create a PonyORM model

    This decorator serves to denote PonyORM models. It automatically
    connects them to your application, and is type-safe.
    """

    def __call__(self, model_cls: Type):

        model = type(model_cls.__name__, (Tulpar.db.Entity,), model_cls.__dict__)

        return model
