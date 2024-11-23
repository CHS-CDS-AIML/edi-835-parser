from typing import Iterator, Tuple, Optional, List
from warnings import warn

from edi_835_parser.edi_837.segments.provider import Provider as ProviderSegment
from edi_835_parser.edi_837.segments.subscriber import Subscriber as SubscriberSegment
from edi_835_parser.edi_837.segments.claim import Claim as ClaimSegment
from edi_835_parser.edi_837.segments.service import Service as ServiceSegment
from edi_835_parser.edi_837.segments.diagnosis_codes import DiagnosisCodes as DiagnosisCodesSegment
from edi_835_parser.edi_837.loops.service import Service as ServiceLoop
from edi_835_parser.edi_837.segments.date import Date as DateSegment

from edi_835_parser.segments.address import Address as AddressSegment
from edi_835_parser.segments.location import Location as LocationSegment
from edi_835_parser.segments.utilities import find_identifier
from edi_835_parser.segments.entity import Entity as EntitySegment
from edi_835_parser.edi_837.segments.reference import Reference as ReferenceSegment
from edi_835_parser.segments.amount import Amount as AmountSegment

class Claim:
    """
    class reprsenting Loop 2300 of 837
    
    """
    initiating_identifier = ClaimSegment.identification
    terminating_identifiers = [ClaimSegment.identification, 
            "HL",
            "SE",
            ]

    def __init__(
        self,
        claim: ClaimSegment = None,
        entities: List[EntitySegment] = None,
        services: List[ServiceLoop] = None,
        references: List[ReferenceSegment] = None,
        dates: List[DateSegment] = None,
        amount: AmountSegment = None,
        diagnosis_codes: DiagnosisCodesSegment = None,
    ):
        self.claim = claim
        self.entities = entities if entities else []
        self.services = services if services else []
        self.references = references if references else []
        self.dates = dates if dates else []
        self.amount = amount
        self.diagnosis_codes = diagnosis_codes

    def __repr__(self):
        return "\n".join(str(item) for item in self.__dict__.items())

    @property
    def rendering_provider(self) -> Optional[EntitySegment]:
        rendering_provider = [
            e for e in self.entities if e.entity == "rendering_provider"
        ]
        assert len(rendering_provider) <= 1

        if len(rendering_provider) == 1:
            return rendering_provider[0]

    @property
    def facility(self) -> Optional[EntitySegment]:
        facility = [
            e for e in self.entities if e.entity == "facility"
        ]
        assert len(facility) <= 1

        if len(facility) == 1:
            return facility[0]

    @property
    def authorization_number(self) -> Optional[ReferenceSegment]:
        auth_number = [
            r for r in self.references if r.qualifier == "authorization_number"
        ]

        assert len(auth_number) <= 1

        if len(auth_number) == 1:
            return auth_number[0]

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
        #statement_period_start = [
        #    d for d in self.dates #if d.qualifier == "claim statement period start"
        #]
        #assert len(statement_period_start) <= 1

        #if len(statement_period_start) == 1:
        #    return statement_period_start[0]
        return None

    @property
    def claim_statement_period_end(self) -> Optional[DateSegment]:
        return None

    #@property
    #def patient(self) -> EntitySegment:
    #    patient = [e for e in self.entities if e.entity == "patient"]
    #    assert len(patient) == 1

    #    return patient[0]

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

                elif identifier == DiagnosisCodesSegment.identification:
                    diagnosis_codes = DiagnosisCodesSegment(segment)
                    claim.diagnosis_codes = diagnosis_codes
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
