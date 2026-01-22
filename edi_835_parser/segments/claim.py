from edi_835_parser.elements.identifier import Identifier
from edi_835_parser.elements.claim_status import ClaimStatus
from edi_835_parser.elements.claim_facility import ClaimFacility
from edi_835_parser.elements.dollars import Dollars
from edi_835_parser.elements.claim_type import ClaimType
from edi_835_parser.elements.claim_frequency import ClaimFrequencyCode
from edi_835_parser.segments.utilities import split_segment


class Claim:
    identification = "CLP"

    identifier = Identifier()
    status = ClaimStatus()
    charge_amount = Dollars()
    paid_amount = Dollars()
    claim_type = ClaimType()

    def __init__(self, segment: str):
        self.segment = segment
        segment = split_segment(segment)

        self.identifier = segment[0]
        self.marker = segment[1]
        self.status = segment[2]
        self.charge_amount = segment[3]
        self.paid_amount = segment[4]
        self.claim_type = segment[6]
        self.icn = segment[7]
        # not all CLP segments will have these elements
        claim_facility = ClaimFacility()
        try:
            facility_value = claim_facility.parser(segment[8])
            self.claim_facility_code = facility_value.code
            self.claim_facility_desc = facility_value.description
        except (IndexError, ValueError):
            self.claim_facility_code = None
            self.claim_facility_desc = None

        claim_frequency = ClaimFrequencyCode()
        try:
            claim_frequency_value = claim_frequency.parser(segment[9])
            self.claim_freq_type = claim_frequency_value.code
            self.claim_freq_desc = claim_frequency_value.description
        except (IndexError, ValueError):
            self.claim_freq_type = None
            self.claim_freq_desc = None

    def __repr__(self):
        return "\n".join(str(item) for item in self.__dict__.items())


if __name__ == "__main__":
    pass
