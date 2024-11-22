from edi_835_parser.elements.identifier import Identifier
from edi_835_parser.elements.entity_code import EntityCode
from edi_835_parser.edi_837.bill_provider import BillProvider
from edi_835_parser.elements.entity_type import EntityType
from edi_835_parser.elements.identification_code_qualifier import (
    IdentificationCodeQualifier,
)
from edi_835_parser.segments.utilities import split_segment, get_element


class Entity:
    identification = "NM1"

    identifier = Identifier()
    entity = EntityCode()
    type = EntityType()
    identification_code_qualifier = IdentificationCodeQualifier()

    def __init__(self, segment: str):
        self.segment = segment
        segment = split_segment(segment)

        try:
            self.identifier = segment[0]
        except IndexError:
            self.identifier = None

        try:
            self.bill_provider = segment[1]
        except IndexError:
            self.bill_provider = None
        try:
            self.entity = segment[2]
        except IndexError:
            self.entity = None
        try:
            self.last_name = segment[3]
        except IndexError:
            self.last_name = None
        try:
            self.first_name = get_element(segment, 4)
        except IndexError:
            self.first_name = None
        try:
            self.identification_code_qualifier = get_element(segment, 8)
        except IndexError:
            self.identification_code_qualifier = None
        try:
            self.identification_code = get_element(segment, 9)
        except IndexError:
            self.identification_code = None

    def __repr__(self):
        return "\n".join(str(item) for item in self.__dict__.items())

    @property
    def name(self) -> str:
        return f"{self.first_name} {self.last_name}".title()


if __name__ == "__main__":
    pass
