from typing import Iterator, Tuple, Optional, List
from warnings import warn

from edi_835_parser.segments.organization import Organization as OrganizationSegment
from edi_835_parser.segments.claim import Claim as ClaimSegment
from edi_835_parser.loops.claim import Claim as ClaimLoop
from edi_835_parser.segments.address import Address as AddressSegment
from edi_835_parser.segments.location import Location as LocationSegment
from edi_835_parser.segments.utilities import find_identifier

class Organization:
    # TODO: Put claim loop in here to get correct hierarchy
    initiating_identifier = OrganizationSegment.identification
    terminating_identifiers = [
        ClaimSegment.identification,
        OrganizationSegment.identification,
        "SE",
    ]

    def __init__(
        self,
        #organization: OrganizationSegment = None,
        location: LocationSegment = None,
        address: AddressSegment = None,
        claims: List[ClaimLoop]  = None,
        payer: OrganizationSegment = None,
        payee: OrganizationSegment = None,
    ):
        #self.organization = organization
        self.payee = payee
        self.payer = payer
        self.location = location
        self.address = address
        self.claims = claims if claims else []

    def __repr__(self):
        return "\n".join(str(item) for item in self.__dict__.items())

    @classmethod
    def build(
        cls, current_segment: str, segments: Iterator[str]
    ) -> Tuple["OrganizationSegment", Optional[Iterator[str]], Optional[str]]:
        organization = Organization()
        #organization.organization = OrganizationSegment(current_segment)
        first_org = OrganizationSegment(current_segment)
        if first_org.type == "payer":
            organization.payer = first_org
            segment_terminating_identifier = "PR"
            other_org = "PE"
        else:
            organization.payee = first_org
            segment_terminating_identifier = "PE"
            other_org = "PR"

        segment = segments.__next__()
        while True:
            try:
                if segment is None:
                    segment = segments.__next__()
                identifier = find_identifier(segment)

                if identifier == ClaimLoop.initiating_identifier:
                    claim, segments, segment = ClaimLoop.build(segment, segments)
                    organization.claims.append(claim)
                    # check if claims has hit end
                    if segments == segment == None:
                        raise StopIteration

                elif identifier == AddressSegment.identification:
                    organization.address = AddressSegment(segment)
                    segment = None

                elif identifier == LocationSegment.identification:
                    organization.location = LocationSegment(segment)
                    segment = None
               
                elif identifier in cls.terminating_identifiers:
                    if identifier == "N1":
                        if segment.split("*")[1] == other_org:
                            if other_org == "PR":
                                organization.payer = OrganizationSegment(segment)
                                segment = None
                            elif other_org == "PE":
                                organization.payee = OrganizationSegment(segment)
                                segment = None
                        elif identifier == segment_terminating_identifier:
                            return organization, segments, segment
                    else:
                        return organization, segments, segment

                else:
                    segment = None
                    message = f"Identifier: {identifier} not handled in claim loop."
                    warn(message)

            except StopIteration:
                return organization, None, None


if __name__ == "__main__":
    pass
