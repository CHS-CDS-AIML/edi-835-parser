from edi_835_parser.elements.identifier import Identifier
from edi_835_parser.edi_837.elements.provider_type import ProviderType
from edi_835_parser.segments.utilities import split_segment


class Provider:
    identification = "PRV"

    identifier = Identifier()
    type = ProviderType()

    def __init__(self, segment: str):
        self.segment = segment
        segment = split_segment(segment)

        self.identifier = segment[0]
        self.type = segment[1]
        try:
            self.identification_code = segment[3]
        except:
            self.identification_code = None

    def __repr__(self):
        return "\n".join(str(item) for item in self.__dict__.items())


if __name__ == "__main__":
    pass
