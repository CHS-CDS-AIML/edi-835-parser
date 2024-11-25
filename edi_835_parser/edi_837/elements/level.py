from edi_835_parser.elements import Element, Code
from typing import Iterator, Tuple, Optional, List

levels = {}

class Level(Element):
    def parser(self, value: str) -> str:
        return levels.get(value, value)
