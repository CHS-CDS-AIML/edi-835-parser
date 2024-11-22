from edi_835_parser.elements.identifier import Identifier
from edi_835_parser.elements.subscriber_type import ServiceLineType
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
        self.type = segment[1]
        try:
            self.id_type = segment[3]
        except:
            self.id_type = None
        try:
            self.identification_code = int(segment[4]) if len(segment) >= 5 else None
        except:
            self.identification_code = None

    def __repr__(self):
        return "\n".join(str(item) for item in self.__dict__.items())


if __name__ == "__main__":
    pass