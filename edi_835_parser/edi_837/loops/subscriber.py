from typing import Iterator, Tuple, Optional, List
from warnings import warn

from edi_835_parser.edi_837.segments.provider import Provider as ProviderSegment
from edi_835_parser.edi_837.segments.subscriber import Subscriber as SubscriberSegment
from edi_835_parser.edi_837.segments.claim import Subscriber as ClaimSegment
from edi_835_parser.edi_837.loops.subscriber import Subscriber as SubscriberLoop
from edi_835_parser.edi_837.loops.subscriber import Claim as ClaimLoop

from edi_835_parser.segments.address import Address as AddressSegment
from edi_835_parser.segments.location import Location as LocationSegment
from edi_835_parser.segments.utilities import find_identifier

#name: NameSegment = None # NM1kj
class Subscriber:
    """Class representing 2000A loop of 837"""
    initiating_identifier = SubscriberSegment.identification
    terminating_identifiers = [
        SubscriberSegment.identification, # SBR
        ClaimSegment.identification # CLM
    ]
    def __init__(
            self,
            subscriber: SubscriberSegment = None # SBR
            address: AddressSegment = None #N3
            claims: List[ClaimSegment] = None CLM
            ):
        self.subscriber = subscriber
        self.address = address
        self.claims = claims if claims else []

    def __repr__(self):
        return "\n".join(str(item) for item in self.__dict__.items())
    @classmethod
    def build(
        cls, current_segment: str, segments: Iterator[str]
    ) -> Tuple["SubscriberSegment", Optional[Iterator[str]], Optional[str]]:
        subscriber = Subscriber()
        subscriber.subscriber = SubscriberSegment(current_segment)

        segment = segments.__next__()
        while True:
            try:
                if segment is None:
                    segment = segments.__next__()
                identifier = find_identifier(segment)

                if identifier == ClaimLoop.initiating_identifier:
                    claim, segments, segment = ClaimLoop.build(segment, segments)
                    subscriber.subscribers.append(claim)
                    # check if claims has hit end
                    #if segments == segment == None:
                    #    raise StopIteration

                elif identifier == AddressSegment.identification:
                    subscriber.address = AddressSegment(segment)
                    segment = None

                elif identifier == LocationSegment.identification:
                    subscriber.location = LocationSegment(segment)
                    segment = None
               
                elif identifier in cls.terminating_identifiers:
                    return subscriber, segments, segment

                else:
                    segment = None
                    message = f"Identifier: {identifier} not handled in provider loop."
                    warn(message)

            except StopIteration:
                return organization, None, None


if __name__ == "__main__":
    pass
