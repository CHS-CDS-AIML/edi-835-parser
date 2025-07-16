from edi_835_parser.elements.identifier import Identifier
from edi_835_parser.edi_837.elements.entity_code import EntityCode
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
            self.identifier = ""
        try:
            self.entity = segment[1]
        except IndexError:
            self.entity = ""
        try:
            self.type = segment[2]
        except IndexError:
            self.type = ""
        try:
            self.last_name = segment[3]
        except IndexError:
            self.last_name = ""
        try:
            self.first_name = get_element(segment, 4)
            if self.first_name is None:
                self.first_name = ""
        except IndexError:
            self.first_name = ""
        try:
            self.identification_code_qualifier = get_element(segment, 8)
        except IndexError:
            self.identification_code_qualifier = ""
        try:
            self.identification_code = get_element(segment, 9)
        except IndexError:
            self.identification_code = ""

    def __repr__(self):
        return "\n".join(str(item) for item in self.__dict__.items())

    @property
    def name(self) -> str:
        return f"{self.first_name} {self.last_name}".title()


if __name__ == "__main__":
    pass
