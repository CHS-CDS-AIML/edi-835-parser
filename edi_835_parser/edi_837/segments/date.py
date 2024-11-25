from edi_835_parser.elements.identifier import Identifier
from edi_835_parser.elements.date import Date
from edi_835_parser.edi_837.elements.date_type import DateType
from edi_835_parser.edi_837.elements.date_code import DateCode
from edi_835_parser.segments.utilities import split_segment

class Date:
    identification = "DTP"

    identifier = Identifier()
    date_code = DateCode()
    date = Date()
    type = DateType()

    def __init__(self, segment: str):
        self.segment = segment
        segment = split_segment(segment)
        self.identifier = segment[0]
        self.code = segment[1]
        self.date = segment[2]

    def __repr__(self):
        return "\n".join(str(item) for item in self.__dict__.items())


if __name__ == "__main__":
    pass
