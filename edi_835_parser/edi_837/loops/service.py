from typing import Tuple, Iterator, Optional, List
from warnings import warn

from edi_835_parser.edi_837.segments.provider import Provider as ProviderSegment
from edi_835_parser.edi_837.segments.subscriber import Subscriber as SubscriberSegment
from edi_835_parser.edi_837.segments.claim import Claim as ClaimSegment
from edi_835_parser.edi_837.segments.service_line import ServiceLine as ServiceLineSegment
from edi_835_parser.edi_837.segments.service import Service as ServiceSegment
from edi_835_parser.edi_837.segments.date import Date as DateSegment

from edi_835_parser.segments.amount import Amount as AmountSegment
from edi_835_parser.segments.address import Address as AddressSegment
from edi_835_parser.segments.location import Location as LocationSegment
from edi_835_parser.segments.utilities import find_identifier
from edi_835_parser.edi_837.segments.reference import Reference as ReferenceSegment
from edi_835_parser.elements.dollars import Dollars

class Service:
    """
    class reprsenting Loop 2400 of 837
    """
    initiating_identifier = ServiceLineSegment.identification
    terminating_identifiers = [
        ServiceLineSegment.identification,
        ClaimSegment.identification,
        "HL",
        "SE",
    ]

    def __init__(
        self,
        service_line: ServiceLineSegment = None,
        service: ServiceSegment = None,
        dates: List[DateSegment] = None,
        references: List[ReferenceSegment] = None,
        amount: AmountSegment = None,
    ):
        self.service_line = service
        self.service = service
        self.dates = dates if dates else []
        self.references = references if references else []
        self.amount = amount

    def __repr__(self):
        return "\n".join(str(item) for item in self.__dict__.items())

    @property
    def allowed_amount(self) -> Optional[Dollars]:
        if self.amount:
            if self.amount.qualifier == "allowed - actual":
                return self.amount.amount

    @property
    def service_date(self) -> Optional[DateSegment]:
        service_date = [d for d in self.dates if d.code == "472"]

        if len(service_date) == 1:
            return service_date[0]

    @property
    def service_period_start(self) -> Optional[DateSegment]:
        service_period_start = [
            d for d in self.dates #if d.qualifier == "service period start"
        ]
        #assert len(service_period_start) <= 1, f"{self.dates}"

        if len(service_period_start) == 1:
            return service_period_start[0]
        else:
            return self.service_date

    @property
    def service_period_end(self) -> Optional[DateSegment]:
        service_period_end = [
            d for d in self.dates #if d.qualifier == "service period end"
        ]
        #assert len(service_period_end) <= 1

        if len(service_period_end) == 1:
            return service_period_end[0]
        else:
            return self.service_date

    @classmethod
    def build(
        cls, segment: str, segments: Iterator[str]
    ) -> Tuple["Service", Optional[str], Optional[Iterator[str]]]:
        service = Service()
        service.service_line = ServiceLineSegment(segment)

        while True:
            try:
                segment = segments.__next__()
                identifier = find_identifier(segment)

                if identifier == ServiceSegment.identification:
                    service_seg = ServiceSegment(segment)
                    service.service = service_seg

                elif identifier == DateSegment.identification:
                    date = DateSegment(segment)
                    service.dates.append(date)

                elif identifier == AmountSegment.identification:
                    service.amount = AmountSegment(segment)

                elif identifier == ReferenceSegment.identification:
                    reference = ReferenceSegment(segment)
                    #if "*EA" in segment:
                    #    import pdb; pdb.set_trace()
                    service.references.append(reference)

                elif identifier in cls.terminating_identifiers:
                    return service, segment, segments

                else:
                    message = f"Identifier: {identifier} not handled in service loop."
                    #warn(message)

            except StopIteration:
                return service, None, None


if __name__ == "__main__":
    pass
