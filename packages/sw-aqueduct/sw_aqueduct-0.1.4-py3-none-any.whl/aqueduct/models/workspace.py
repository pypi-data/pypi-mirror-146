# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)

from typing import (
    AnyStr,
    List
)
from attr import (
    define,
    field
)


@define
class Workspace:
    createdDate: AnyStr = field(eq=False)
    modifiedDate: AnyStr = field(eq=False)
    uid: AnyStr = field()
    version: int = field(eq=False)
    id: AnyStr = field()
    disabled: bool = field()
    name: AnyStr = field()
    description: AnyStr = field(default=None)
    dashboards: List = field(default=[])
    applications: List = field(default=[])
    permissions: dict = field(default={}, eq=False)
    createdByUser: dict = field(default={}, eq=False)
    modifiedByUser: dict = field(default={}, eq=False)

    def __init__(self, **kwargs):
        from ..base import Base
        from ..utils.exceptions import ModelError
        Base().scrub(kwargs)
        try:
            self.__attrs_init__(**kwargs)
        except TypeError as te:
            raise ModelError(err=te, name='Workspace')
