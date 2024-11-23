from edi_835_parser.elements import Element, Code
from typing import Iterator, Tuple, Optional, List

hierarchy_types = {
        "1": "subscriber",
        "2": "patient",
        "3": "dependent",
        "4": "provider",
        "5": "payee",
        }

class HierarchyType(Element):
    def parser(self, value: str) -> str:
        return hierarchy_types.get(value, value)
