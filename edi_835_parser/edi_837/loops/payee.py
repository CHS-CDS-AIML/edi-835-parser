from typing import Iterator, Tuple, Optional, List
from warnings import warn

from edi_835_parser.segments.organization import Organization as OrganizationSegment
from edi_835_parser.segments.entity import Entity as EntitySegment
from edi_835_parser.segments.provider_summary import ProviderSummary as ProviderSummarySegment
from edi_835_parser.segments.reference import Reference as ReferenceSegment
from edi_835_parser.segments.date import Date as DateSegment
from edi_835_parser.segments.amount import Amount as AmountSegment
from edi_835_parser.segments.utilities import find_identifier
from edi_835_parser.segments.remark import Remark as RemarkSegment
from edi_835_parser.loops.service import Service as ServiceLoop
from edi_835_parser.segments.service_adjustment import (
    ServiceAdjustment as ServiceAdjustmentSegment,
)


class Payee:
    initiating_identifier = "N1"
    terminating_identifiers = ["N1", "SE"]

    def __init__(
        self,
        organization: OrganizationSegment = None,
    ):
        self.organization = organization

    def __repr__(self):
        return "\n".join(str(item) for item in self.__dict__.items())

    @classmethod
    def build(
        cls, segment: str, segments: Iterator[str]
    ) -> Tuple["Payee", Optional[Iterator[str]], Optional[str]]:
        payee = Payee()

        segment = segments.__next__()
        while True:
            try:
                if segment is None:
                    segment = segments.__next__()

                identifier = find_identifier(segment)

                if identifier == OrganizationSegment.identification:
                    org = OrganizationSegment(segment)
                    payee.organization_segment = org
                    segment = None

                elif identifier in cls.terminating_identifiers:
                    return payee, segments, segment

                else:
                    segment = None
                    message = f"Identifier: {identifier} not handled in payee loop."
                    warn(message)

            except StopIteration:
                return payee, None, None
