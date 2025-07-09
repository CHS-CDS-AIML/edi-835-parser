from typing import List, Iterator, Optional
from collections import namedtuple

import pandas as pd

from edi_835_parser.edi_837.loops.claim import Claim as ClaimLoop
from edi_835_parser.edi_837.loops.service import Service as ServiceLoop
from edi_835_parser.edi_837.loops.provider import Provider as ProviderLoop
from edi_835_parser.edi_837.loops.subscriber import Subscriber as SubscriberLoop
from edi_835_parser.segments.utilities import find_identifier
from edi_835_parser.segments.interchange import Interchange as InterchangeSegment
from edi_835_parser.segments.financial_information import (
    FinancialInformation as FinancialInformationSegment,
)

BuildAttributeResponse = namedtuple(
    "BuildAttributeResponse", "key value segment segments"
)


class TransactionSet:

    def __init__(
        self,
        interchange: InterchangeSegment,
        financial_information: FinancialInformationSegment,
        providers: List[ProviderLoop],
        subscribers: List[SubscriberLoop],
        claims: List[ClaimLoop],
        service_lines: List[ServiceLoop],
        file_path: str,
    ):
        self.interchange = interchange
        self.financial_information = financial_information
        self.providers = providers
        self.subscribers = subscribers
        self.claims = claims
        self.service_lines = service_lines
        self.file_path = file_path

    def __repr__(self):
        return "\n".join(str(item) for item in self.__dict__.items())

    def to_dataframe(self) -> pd.DataFrame:
        """flatten the remittance advice by service to a pandas DataFrame"""
        data = []
        for provider in self.providers:
            for subscriber in provider.subscribers:
                if subscriber.subscriber is None:
                    continue
                for claim in subscriber.claims:
                    for service in claim.services:
                        datum = TransactionSet.serialize_service(
                            self.financial_information, provider, subscriber, claim, service
                        )

                        data.append(datum)
        df = pd.DataFrame(data)

        return df

    @staticmethod
    def serialize_service(
        financial_information: FinancialInformationSegment,
        provider: ProviderLoop,
        subscriber: SubscriberLoop,
        claim: ClaimLoop,
        service: ServiceLoop,
    ) -> dict:
        # if the service doesn't have a start date assume the service and claim dates match
        start_date = None
        start_date_type = None
        if service.service_period_start:
            start_date = service.service_period_start.date
            start_date_type = "service_period"
        elif claim.claim_statement_period_start:
            start_date = claim.claim_statement_period_start.date
            start_date_type = "claim_statement"

        # if the service doesn't have an end date assume the service and claim dates match
        end_date = None
        end_date_type = None
        if service.service_period_end:
            end_date = service.service_period_end.date
            end_date_type = "service_period"
        elif claim.claim_statement_period_end:
            end_date = claim.claim_statement_period_end.date
            end_date_type = "claim_statement"

        ea_code = None
        for reference in claim.references:
            if reference._qualifier.code == "EA":
                ea_code = reference.value

        if provider is None:
            billing_id_code = None
        else:
            billing_id_code = provider.provider.identification_code
        # determine billing provider and npi
        if provider.name is None:
            billing_provider = None
            billing_npi = None
        else:
            billing_provider = provider.name.last_name
            if provider.name._identification_code_qualifier == "national provider id":
                billing_npi = provider.name.identification_code
            else:
                billing_npi = None
        if provider.pay_to_provider is None:
            ptp = None
        else:
            ptp = provider.pay_to_provider.last_name
        if service.service is None:
            charge_amount = None
        else:
            charge_amount = service.service.charge_amount

        datum = {
            "patient_identifier": ea_code,
            "billing_id_code": billing_id_code,
            "billing_provider": billing_provider,
            "pay_to_provider": ptp,
            "subscriber_responsibility": subscriber.subscriber.responsibility,
            "subscriber_relationship": subscriber.subscriber.relationship,
            "subscriber_group_number": subscriber.subscriber.group_number,
            "subscriber_plan": subscriber.subscriber.plan,
            "subscriber_name": subscriber.patient.first_name + " " + subscriber.patient.last_name,
            "subscriber_code_qualifier": subscriber.patient.identification_code_qualifier,
            "subscriber_code": subscriber.patient.identification_code,
            "subscriber_dob": str(subscriber.demographic.dob),
            # TODO: Get demographic
            "subscriber_payer": subscriber.payer.last_name,
            "claim_rendering_provider": claim.rendering_provider,
            "facility": claim.facility.last_name if claim.facility else None,
            "facility_npi": billing_npi,
            "claim_identifier": claim.claim.claim_identifier,
            "claim_amount": claim.claim.claim_amount,
            "authorization_number": claim.authorization_number,
            "dx_codes": [{"code": i.code, "description": i.description} for i in claim.diagnosis_codes.diagnosis_codes],
            "charge_amount": charge_amount,
        }

        return datum

    @classmethod
    def build(cls, file_path: str) -> "TransactionSet":
        interchange = None
        financial_information = None
        providers = []
        subscribers = []
        claims = []
        service_lines = []

        try:
            with open(file_path) as f:
                file = f.read()
        except UnicodeDecodeError:
            print("failed")
            return None
            

        segments = file.split("~")
        segments = [segment.strip() for segment in segments]

        segments = iter(segments)
        segment = None

        while True:
            response = cls.build_attribute(segment, segments)
            segment = response.segment
            segments = response.segments

            # no more segments to parse
            if response.segments is None:
                break

            if response.key == "interchange":
                interchange = response.value

            if response.key == "financial information":
                financial_information = response.value

            if response.key == "provider":
                providers.append(response.value)

            if response.key == "subscriber":
                subscribers.append(response.value)

            if response.key == "claim":
                claims.append(response.value)

            if response.key == "service":
                service_lines.append(response.value)

        return TransactionSet(
            interchange, financial_information, providers, subscribers, claims, service_lines, file_path
        )

    @classmethod
    def build_attribute(
        cls, segment: Optional[str], segments: Iterator[str]
    ) -> BuildAttributeResponse:
        if segment is None:
            try:
                segment = segments.__next__()
            except StopIteration:
                return BuildAttributeResponse(None, None, None, None)

        identifier = find_identifier(segment)
        all_sub_segments = segment.split("*")

        if identifier == InterchangeSegment.identification:
            interchange = InterchangeSegment(segment)
            return BuildAttributeResponse("interchange", interchange, None, segments)

        if identifier == FinancialInformationSegment.identification:
            financial_information = FinancialInformationSegment(segment)
            return BuildAttributeResponse(
                "financial information", financial_information, None, segments
            )

        if identifier == ProviderLoop.initiating_identifier and segment.split("*")[2] == "":
            provider, segments, segment = ProviderLoop.build(segment, segments)
            return BuildAttributeResponse(
                "provider", provider, segment, segments
            )

        elif identifier in SubscriberLoop.initiating_identifier:
            if identifier == "HL" and segment.split("*")[3] != "22":
                pass
            else:
               subscriber, segments, segment = SubscriberLoop.build(segment, segments)
               return BuildAttributeResponse(
                   "subscriber", subscriber, segment, segments
               )

        elif identifier == ClaimLoop.initiating_identifier:
            claim, segments, segment = ClaimLoop.build(segment, segments)
            return BuildAttributeResponse("claim", claim, segment, segments)

        elif identifier == ServiceLoop.initiating_identifier:
            service, segments, segment = ServiceLoop.build(segment, segments)
            return BuildAttributeResponse("service", service, segment, segments)

        else:
            return BuildAttributeResponse(None, None, None, segments)


if __name__ == "__main__":
    pass
