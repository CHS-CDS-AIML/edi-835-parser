from edi_835_parser.elements.identifier import Identifier
from edi_835_parser.elements.date import Date
from edi_835_parser.segments.utilities import split_segment


class Demographic:
    identification = "DMG"

    identifier = Identifier()
    dob = Date()

    def __init__(self, segment: str):
        self.segment = segment
        segment = split_segment(segment)
        self.identifier = segment[0]
        self.id = segment[1]
        self.dob = segment[2]

    def __repr__(self):
        return "\n".join(str(item) for item in self.__dict__.items())


if __name__ == "__main__":
    pass
