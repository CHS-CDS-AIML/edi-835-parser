from edi_835_parser.elements.identifier import Identifier
from edi_835_parser.segments.utilities import split_segment
from edi_835_parser.edi_837.elements.parent import Parent
from edi_835_parser.edi_837.elements.child import Child
from edi_835_parser.edi_837.elements.level import Level
from edi_835_parser.edi_837.elements.hierarchy_type import HierarchyType


class Hierarchy:
    identification = "HL"

    identifier = Identifier()
    level = Level()
    parent = Parent()
    hierarchy_type = HierarchyType()
    child = Child()

    def __init__(self, segment: str):
        self.segment = segment
        segment = split_segment(segment)
        self.identifier = segment[0]
        self.level = segment[1]
        self.parent = segment[2]
        self.hierarchy_type = segment[3]
        self.child = segment[4]

    def __repr__(self):
        return "\n".join(str(item) for item in self.__dict__.items())


if __name__ == "__main__":
    pass
