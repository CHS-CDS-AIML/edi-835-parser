from edi_835_parser.elements import Element, Code
from typing import Iterator, Tuple, Optional, List

parents = {}

class Parent(Element):
    def parser(self, value: str) -> str:
        return parents.get(value, value)
