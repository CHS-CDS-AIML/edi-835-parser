from edi_835_parser.elements.identifier import Identifier
from edi_835_parser.edi_837.elements.service_line_type import ServiceLineType
from edi_835_parser.segments.utilities import split_segment


class ServiceLine:
    """
    class representing service line segment

    *
    DATE DTP
    Reference REF
    Note NTE

    """
    identification = "LX"

    identifier = Identifier()
    type = ServiceLineType()

    def __init__(self, segment: str):
        self.segment = segment
        segment = split_segment(segment)

        self.identifier = segment[0]
        self.line = segment[1] # CPT code, need to furhter parse

    def __repr__(self):
        return "\n".join(str(item) for item in self.__dict__.items())


if __name__ == "__main__":
    pass
