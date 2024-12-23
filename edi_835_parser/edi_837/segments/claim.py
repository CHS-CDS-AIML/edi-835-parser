from edi_835_parser.elements.identifier import Identifier
from edi_835_parser.elements.claim_status import ClaimStatus
from edi_835_parser.elements.dollars import Dollars
from edi_835_parser.elements.claim_type import ClaimType
from edi_835_parser.segments.utilities import split_segment


class Claim:
    identification = "CLM"

    identifier = Identifier()
    claim_amount = Dollars()

    def __init__(self, segment: str):
        self.segment = segment
        segment = split_segment(segment)
        self.identifier = segment[0]
        self.claim_identifier = segment[1]
        self.claim_amount = segment[2]

    def __repr__(self):
        return "\n".join(str(item) for item in self.__dict__.items())


if __name__ == "__main__":
    pass
