from edi_835_parser.elements.identifier import Identifier
from edi_835_parser.edi_837.elements.service_type import ServiceLineType
from edi_835_parser.segments.utilities import split_segment


class ServiceLine:
    """
    class representing service line segment

    *
    DATE DTP
    Reference REF
    Note NTE

    """
    identification = "SV1"

    identifier = Identifier()
    type = ServiceLineType()

    def __init__(self, segment: str):
        self.segment = segment
        segment = split_segment(segment)

        self.identifier = segment[0]
        self.cpt = segment[1] # CPT code, need to furhter parse
        self.charge_amount = segment[2]
        self.measurement = segment[3]
        self.quantity = segment[4]
        self.facility_code = segment[5]
        self.diagnosis_code_pointer = segment[6]
        #try:
        #    self.identification_code = int(segment[4]) if len(segment) >= 5 else None
        #except:
        #    self.identification_code = None

    def __repr__(self):
        return "\n".join(str(item) for item in self.__dict__.items())


if __name__ == "__main__":
    pass
