from edi_835_parser.elements import Element, Code
from typing import Iterator, Tuple, Optional, List

children = {}

class Child(Element):
    def parser(self, value: str) -> str:
        return children.get(value, value)
