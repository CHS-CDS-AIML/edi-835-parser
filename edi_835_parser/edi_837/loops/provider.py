from typing import Iterator, Tuple, Optional, List
from warnings import warn

from edi_835_parser.edi_837.segments.provider import Provider as ProviderSegment
from edi_835_parser.edi_837.segments.subscriber import Subscriber as SubscriberSegment
from edi_835_parser.edi_837.loops.subscriber import Subscriber as SubscriberLoop
from edi_835_parser.edi_837.segments.hierarchy import Hierarchy as HierarchySegment
from edi_835_parser.edi_837.segments.entity import Entity as EntitySegment

from edi_835_parser.segments.address import Address as AddressSegment
from edi_835_parser.segments.location import Location as LocationSegment
from edi_835_parser.edi_837.segments.reference import Reference as ReferenceSegment
from edi_835_parser.segments.utilities import find_identifier


#name: NameSegment = None # NM1kj
class Provider:
    """Class representing 2000A loop of 837

    Needs
    address - ok
    location (n4) - ok
    ref (ref) - ok
    """
    initiating_identifier = HierarchySegment.identification
    initiating_parent = ""
    terminating_identifiers = [
        HierarchySegment.identification,
        "SE",
        "IEA",
    ]
    terminating_parent = ""
    def __init__(
            self,
            provider: ProviderSegment = None, # PRV
            hierarchy: HierarchySegment = None,
            address: AddressSegment = None, #N3
            subscribers: SubscriberSegment = None, #HL
            location: LocationSegment = None,
            reference: ReferenceSegment = None,
            entities: List[EntitySegment] = None,
            ):
        self.provider = provider
        self.hierarchy = hierarchy
        self.address = address
        self.subscribers = subscribers if subscribers else []
        self.location = location
        self.reference = reference
        self.entities = entities if entities else []

    def __repr__(self):
        return "\n".join(str(item) for item in self.__dict__.items())

    @property
    def name(self) -> Optional[EntitySegment]:
        name = [
                e for e in self.entities if e.entity == "billing_provider"# TODO: Get entity name
        ]
        assert len(name) <= 1

        if len(name) == 1:
            return name[0]

    @property
    def pay_to_provider(self) -> Optional[EntitySegment]:
        name = [
                e for e in self.entities if e.entity == "pay_to_provider"# TODO: Get entity name
        ]
        assert len(name) <= 1

        if len(name) == 1:
            return name[0]

    @classmethod
    def build(
        cls, current_segment: str, segments: Iterator[str]
    ) -> Tuple["ProviderSegment", Optional[Iterator[str]], Optional[str]]:
        provider = Provider()
        provider.hierarchy = HierarchySegment(current_segment)
        segment = segments.__next__()
        identifier = find_identifier(segment)
        if identifier != "PRV":
            return provider, None, None
        provider.provider = ProviderSegment(segment)
        segment = segments.__next__()

        while True:
            try:
                if segment is None:
                    segment = segments.__next__()
                identifier = find_identifier(segment)

                if identifier in SubscriberLoop.initiating_identifier and segment.split("*")[3] == SubscriberLoop.initiating_type:
                    subscriber, segments, segment = SubscriberLoop.build(segment, segments)
                    provider.subscribers.append(subscriber)
                    # check if claims has hit end
                    if segments == segment == None:
                        raise StopIteration

                elif identifier == AddressSegment.identification:
                    provider.address = AddressSegment(segment)
                    segment = None

                elif identifier == LocationSegment.identification:
                    provider.location = LocationSegment(segment)
                    segment = None

                elif identifier == EntitySegment.identification:
                    entity = EntitySegment(segment)
                    provider.entities.append(entity)
                    segment = None

                elif identifier == ReferenceSegment.identification:
                    provider.reference = ReferenceSegment(segment)
                    segment = None
               
                elif identifier in cls.terminating_identifiers:
                    if segment.split("*")[1] == "AT":
                        message = f"Identifier: {identifier} not handled in provider loop."
                        #warn(message)
                        segment = None
                    elif identifier == "HL":
                        if segment.split("*")[2] == cls.terminating_parent:
                            return provider, segments, segment
                        else:
                            message = f"identifier: {identifier} not handled in provider loop."
                            #warn(message)
                            segment = None
                    else:
                        return provider, segments, segment

                else:
                    segment = None
                    message = f"Identifier: {identifier} not handled in provider loop."
                    #warn(message)

            except StopIteration:
                return provider, None, None


if __name__ == "__main__":
    pass
