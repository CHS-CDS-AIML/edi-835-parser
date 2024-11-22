from edi_835_parser.elements.identifier import Identifier
from edi_835_parser.edi_837.elements.service_type import ServiceType
from edi_835_parser.segments.utilities import split_segment


class Service:
    """
    class representing service line segment

    *
    DATE DTP
    Reference REF
    Note NTE

    """
    identification = "SV2"

    identifier = Identifier()
    type = ServiceType()

    def __init__(self, segment: str):
        self.segment = segment
        segment = split_segment(segment)

        self.identifier = segment[0]
        try:
            self.cpt = segment[1] # CPT code, need to furhter parse
        except IndexError:
            self.cpt = None
        try:
            self.charge_amount = segment[2]
        except IndexError:
            self.charge_amount = None
        try:
            self.measurement = segment[3]
        except IndexError:
            self.measurement = None
        try:
            self.quantity = segment[4]
        except IndexError:
            self.quantity = None
        try:
            self.facility_code = segment[5]
        except IndexError:
            self.facility_code = None
        try:
            self.diagnosis_code_pointer = segment[6]
        except IndexError:
            self.diagnosis_code_pointer = None

    def __repr__(self):
        return "\n".join(str(item) for item in self.__dict__.items())


if __name__ == "__main__":
    pass
