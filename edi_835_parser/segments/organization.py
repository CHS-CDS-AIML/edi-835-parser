from edi_835_parser.elements.identifier import Identifier
from edi_835_parser.elements.organization_type import OrganizationType
from edi_835_parser.segments.utilities import split_segment


class Organization:
    identification = "N1"

    identifier = Identifier()
    type = OrganizationType()

    def __init__(self, segment: str):
        self.segment = segment
        segment = split_segment(segment)

        self.identifier = segment[0]
        if segment[1] == "PR":
            self.type = "payer"
        elif segment[1] == "PE":
            self.type = "payee"
        self.name = segment[2]
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
