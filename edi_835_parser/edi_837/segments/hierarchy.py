from edi_835_parser.elements.identifier import Identifier
from edi_835_parser.segments.utilities import split_segment


class Hierarchy:
    identification = "HL"

    identifier = Identifier()

    def __init__(self, segment: str):
        self.segment = segment
        segment = split_segment(segment)
        self.identifier = segment[0]

    def __repr__(self):
        return "\n".join(str(item) for item in self.__dict__.items())


if __name__ == "__main__":
    pass
