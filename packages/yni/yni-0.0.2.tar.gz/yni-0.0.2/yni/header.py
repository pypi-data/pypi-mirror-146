from typing import Any, Dict, List
from dataclasses import dataclass, field


ORIGINAL_SETATTR = object.__setattr__
ORIGINAL_GETATTR = object.__getattribute__


class BaseClass:
    attributes: Dict[str, Any]

    def __getitem__(self, name: str):
        return self.attributes[name]

    def __setitem__(self, name: str, value: Any):
        self.attributes[name] = value

    def __getattribute__(self, __name: str) -> Any:
        orig = super().__getattribute__
        try:
            return orig(__name)
        except AttributeError:
            return self[__name]

    def __setattr__(self, __name: str, __value: Any) -> None:
        orig = super().__getattribute__
        try:
            if __name in orig("attributes"):
                self[__name] = __value
        except AttributeError:
            pass
        return super().__setattr__(__name, __value)


@dataclass
class Header(BaseClass):
    name: str
    attributes: Dict[str, Any] = field(default_factory=dict)
    children: "List[Child]" = field(default_factory=list)


@dataclass
class Child(BaseClass):
    parent: Header
    name: str
    attributes: Dict[str, Any] = field(default_factory=dict)
