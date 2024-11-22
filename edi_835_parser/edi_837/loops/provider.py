from typing import Iterator, Tuple, Optional, List
from warnings import warn

from edi_835_parser.edi_837.segments.provider import Provider as ProviderSegment
from edi_835_parser.edi_837.segments.subscriber import Subscriber as SubscriberSegment
from edi_835_parser.edi_837.loops.subscriber import Subscriber as SubscriberLoop
from edi_835_parser.edi_837.segments.hierarchy import Hierarchy as HierarchySegment

from edi_835_parser.segments.address import Address as AddressSegment
from edi_835_parser.segments.location import Location as LocationSegment
from edi_835_parser.segments.reference import Reference as ReferenceSegment
from edi_835_parser.segments.utilities import find_identifier


#name: NameSegment = None # NM1kj
class Provider:
    """Class representing 2000A loop of 837

    Needs
    address - ok
    location (n4) - ok
    ref (ref) - ok
    contact (PER) - not completed but don't think we need
    """
    initiating_identifier = HierarchySegment.identification
    terminating_identifiers = [
        #ProviderSegment.identification, # PRV
        HierarchySegment.identification,
        "SE"
    ]
    def __init__(
            self,
            provider: ProviderSegment = None, # PRV
            hierarchy: HierarchySegment = None,
            address: AddressSegment = None, #N3
            subscribers: SubscriberSegment = None, #HL
            location: LocationSegment = None,
            reference: ReferenceSegment = None,
            ):
        self.provider = provider
        self.hierarchy = hierarchy
        self.address = address
        self.subscribers = subscribers if subscribers else []
        self.location = location
        self.reference = reference

    def __repr__(self):
        return "\n".join(str(item) for item in self.__dict__.items())
    @classmethod
    def build(
        cls, current_segment: str, segments: Iterator[str]
    ) -> Tuple["ProviderSegment", Optional[Iterator[str]], Optional[str]]:
        provider = Provider()
        provider.hierarchy = HierarchySegment(current_segment)

        segment = segments.__next__()
        while True:
            try:
                if segment is None:
                    try:
                        segment = segments.__next__()
                    except:
                        import pdb; pdb.set_trace()
                identifier = find_identifier(segment)
          
                if identifier == ProviderSegment.identification:
                    provider.provider = ProviderSegment(segment)
                    segment = None

                elif identifier == SubscriberLoop.initiating_identifier:
                    subscriber, segments, segment = SubscriberLoop.build(segment, segments)
                    provider.subscribers.append(subscriber)
                    # check if claims has hit end
                    #if segments == segment == None:
                    #    raise StopIteration

                elif identifier == AddressSegment.identification:
                    provider.address = AddressSegment(segment)
                    segment = None

                elif identifier == LocationSegment.identification:
                    provider.location = LocationSegment(segment)
                    segment = None

                elif identifier == ReferenceSegment.identification:
                    provider.reference = ReferenceSegment(segment)
                    segment = None
               
                elif identifier in cls.terminating_identifiers:
                    # TODO: Need to handle PRV segment in Claim (PRV*PE)
                    if segment.split("*")[1] == "AT":
                        message = f"Identifier: {identifier} not handled in provider loop."
                        warn(message)
                    else:
                        return organization, segments, segment

                else:
                    segment = None
                    message = f"Identifier: {identifier} not handled in provider loop."
                    warn(message)

            except StopIteration:
                return organization, None, None


if __name__ == "__main__":
    pass
