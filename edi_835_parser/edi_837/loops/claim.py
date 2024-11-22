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

class Claim:
    """
    class reprsenting Loop 2300 of 837
    
    """
    initiating_identifier = ClaimSegment.identification
    terminating_identifiers = [ClaimSegment.identification, 
            ServiceSegment.identification,
            "SE"]

    def __init__(
        self,
        claim: ClaimSegment = None,
        entities: List[EntitySegment] = None,
        services: List[ServiceLoop] = None,
        references: List[ReferenceSegment] = None,
        dates: List[DateSegment] = None,
        amount: AmountSegment = None,
        self.diagnosis_codes = List[DiagnosisCode] = None,
    ):
        self.claim = claim
        self.entities = entities if entities else []
        self.services = services if services else []
        self.references = references if references else []
        self.dates = dates if dates else []
        self.amount = amount
        self.diagnosis_codes = diagnosis_codes if diagnosis_codes else []

    def __repr__(self):
        return "\n".join(str(item) for item in self.__dict__.items())

    @property
    def rendering_provider(self) -> Optional[EntitySegment]:
        rendering_provider = [
            e for e in self.entities if e.entity == "rendering provider"
        ]
        assert len(rendering_provider) <= 1

        if len(rendering_provider) == 1:
            return rendering_provider[0]

    @property
    def provider(self) -> Optional[EntitySegment]:
        rendering_provider = [
            e for e in self.entities if e.entity == "provider" #PRV
        ]
        assert len(rendering_provider) <= 1

        if len(rendering_provider) == 1:
            return rendering_provider[0]

    @property
    def claim_statement_period_start(self) -> Optional[DateSegment]:
        statement_period_start = [
            d for d in self.dates if d.qualifier == "claim statement period start"
        ]
        assert len(statement_period_start) <= 1

        if len(statement_period_start) == 1:
            return statement_period_start[0]

    @property
    def claim_statement_period_end(self) -> Optional[DateSegment]:
        statement_period_end = [
            d for d in self.dates if d.qualifier == "claim statement period end"
        ]
        assert len(statement_period_end) <= 1

        if len(statement_period_end) == 1:
            return statement_period_end[0]

    @property
    def patient(self) -> EntitySegment:
        patient = [e for e in self.entities if e.entity == "patient"]
        assert len(patient) == 1

        return patient[0]

    @classmethod
    def build(
        cls, segment: str, segments: Iterator[str]
    ) -> Tuple["Claim", Optional[Iterator[str]], Optional[str]]:
        claim = Claim()
        claim.claim = ClaimSegment(segment)

        segment = segments.__next__()
        while True:
            try:
                if segment is None:
                    segment = segments.__next__()

                identifier = find_identifier(segment)

                if identifier == ServiceLoop.initiating_identifier:
                    service, segment, segments = ServiceLoop.build(segment, segments)
                    claim.services.append(service)

                elif identifier == EntitySegment.identification:
                    entity = EntitySegment(segment)
                    claim.entities.append(entity)
                    segment = None

                elif identifier == ReferenceSegment.identification:
                    reference = ReferenceSegment(segment)
                    claim.references.append(reference)
                    segment = None

                elif identifier == DateSegment.identification:
                    date = DateSegment(segment)
                    claim.dates.append(date)
                    segment = None

                elif identifier == AmountSegment.identification:
                    amount = AmountSegment(segment)
                    claim.amount = amount
                    segment = None

                elif identifier in cls.terminating_identifiers:
                    return claim, segments, segment

                else:
                    segment = None
                    message = f"Identifier: {identifier} not handled in claim loop."
                    warn(message)

            except StopIteration:
                return claim, None, None
