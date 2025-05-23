from typing import Tuple, Iterator, Optional, List
from warnings import warn

from edi_835_parser.segments.service import Service as ServiceSegment
from edi_835_parser.segments.claim import Claim as ClaimSegment
from edi_835_parser.segments.date import Date as DateSegment
from edi_835_parser.segments.reference import Reference as ReferenceSegment
from edi_835_parser.segments.amount import Amount as AmountSegment
from edi_835_parser.segments.service_adjustment import (
    ServiceAdjustment as ServiceAdjustmentSegment,
)
from edi_835_parser.segments.remark import Remark as RemarkSegment
from edi_835_parser.segments.utilities import find_identifier
from edi_835_parser.elements.dollars import Dollars


class Service:
    initiating_identifier = ServiceSegment.identification
    terminating_identifiers = [
        ServiceSegment.identification,
        ClaimSegment.identification,
        "SE",
    ]

    def __init__(
        self,
        service: ServiceSegment = None,
        dates: List[DateSegment] = None,
        references: List[ReferenceSegment] = None,
        remarks: List[RemarkSegment] = None,
        amount: AmountSegment = None,
        adjustments: List[ServiceAdjustmentSegment] = None,
    ):
        self.service = service
        self.dates = dates if dates else []
        self.references = references if references else []
        self.remarks = remarks if remarks else []
        self.amount = amount
        self.adjustments = adjustments if adjustments else []

    def __repr__(self):
        return "\n".join(str(item) for item in self.__dict__.items())

    @property
    def allowed_amount(self) -> Optional[Dollars]:
        if self.amount:
            if self.amount.qualifier == "allowed - actual":
                return self.amount.amount

    @property
    def service_date(self) -> Optional[DateSegment]:
        service_date = [d for d in self.dates if d.qualifier == "service"]
        assert len(service_date) <= 1, f"{self.dates}"

        if len(service_date) == 1:
            return service_date[0]

    @property
    def service_period_start(self) -> Optional[DateSegment]:
        service_period_start = [
            d for d in self.dates if d.qualifier == "service period start"
        ]
        assert len(service_period_start) <= 1, f"{self.dates}"

        if len(service_period_start) == 1:
            return service_period_start[0]
        else:
            return self.service_date

    @property
    def service_period_end(self) -> Optional[DateSegment]:
        service_period_end = [
            d for d in self.dates if d.qualifier == "service period end"
        ]
        assert len(service_period_end) <= 1

        if len(service_period_end) == 1:
            return service_period_end[0]
        else:
            return self.service_date

    @classmethod
    def build(
        cls, segment: str, segments: Iterator[str]
    ) -> Tuple["Service", Optional[str], Optional[Iterator[str]]]:
        service = Service()
        service.service = ServiceSegment(segment)

        while True:
            try:
                segment = segments.__next__()
                identifier = find_identifier(segment)

                if identifier == DateSegment.identification:
                    date = DateSegment(segment)
                    service.dates.append(date)

                elif identifier == AmountSegment.identification:
                    service.amount = AmountSegment(segment)

                elif identifier == RemarkSegment.identification:
                    remark = RemarkSegment(segment)
                    service.remarks.append(remark)

                elif identifier == ReferenceSegment.identification:
                    reference = ReferenceSegment(segment)
                    #if "*EA" in segment:
                    #    import pdb; pdb.set_trace()
                    service.references.append(reference)

                elif identifier == ServiceAdjustmentSegment.identification:
                    service.adjustments.append(ServiceAdjustmentSegment(segment))

                elif identifier in cls.terminating_identifiers:
                    return service, segment, segments

                else:
                    message = f"Identifier: {identifier} not handled in service loop."
                    warn(message)

            except StopIteration:
                return service, None, None


if __name__ == "__main__":
    pass
