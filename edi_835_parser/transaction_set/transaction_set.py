from typing import List, Iterator, Optional
from collections import namedtuple

import pandas as pd

from edi_835_parser.loops.claim import Claim as ClaimLoop
from edi_835_parser.loops.service import Service as ServiceLoop
from edi_835_parser.loops.organization import Organization as OrganizationLoop
from edi_835_parser.segments.utilities import find_identifier
from edi_835_parser.segments.interchange import Interchange as InterchangeSegment
from edi_835_parser.segments.date import Date as DateSegment
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
        processed_date: DateSegment,
        claims: List[ClaimLoop],
        organizations: List[OrganizationLoop],
        file_path: str,
    ):
        self.interchange = interchange
        self.financial_information = financial_information
        self.processed_date = processed_date
        self.claims = claims
        self.organizations = organizations
        self.file_path = file_path

    def __repr__(self):
        return "\n".join(str(item) for item in self.__dict__.items())

    #@property
    #def payer(self) -> OrganizationLoop:
    #    payer = [o for o in self.organizations if o.organization.type == "payer"]
    #    #assert len(payer) == 1
    #    return payer[0]

    #@property
    #def payee(self) -> OrganizationLoop:
    #    payee = [o for o in self.organizations if o.organization.type == "payee"]
    #    if len(payee) != 1:
    #        payee_list = []
    #        for i in payee:
    #            facility_npi = i.organization.identification_code
    #            payee_list.append(facility_npi)
    #        payee_list = list(set(payee_list))
    #        # TODO: Determine if we need to handle these somehow
    #        #if len(payee_list) > 1:
    #        #    pass
    #    return payee[0]

    def to_dataframe(self) -> pd.DataFrame:
        """flatten the remittance advice by service to a pandas DataFrame"""
        data = []
        for org in self.organizations:
            for claim in org.claims:
                for service in claim.services:
                    datum = TransactionSet.serialize_service(
                        self.financial_information, self.processed_date, org, claim, service
                    )
                    datum["loop"] = "service"

                    for index, adjustment in enumerate(service.adjustments):
                        datum[f"adj_{index}_group"] = adjustment.group_code.code
                        datum[f"adj_{index}_code"] = adjustment.reason_code.code
                        datum[f"adj_{index}_amount"] = adjustment.amount

                    for index, reference in enumerate(service.references):
                        datum[f"ref_{index}_qual"] = reference.qualifier.code
                        datum[f"ref_{index}_value"] = reference.value

                    for index, remark in enumerate(service.remarks):
                        datum[f"rem_{index}_qual"] = remark.qualifier.code
                        datum[f"rem_{index}_code"] = remark.code.code

                    data.append(datum)

                if len(claim.services) == 0:
                    datum = TransactionSet.serialize_claim(
                        self.financial_information, self.processed_date, org, claim
                    )
                    datum["loop"] = "claim"

                    adjs = list()
                    rems = list()
                    for index, adjustment in enumerate(claim.adjustments):
                        #TODO: Figure out logic for actually passing in claim codes with amount. Right now just adding the common ones without amounts
                        adjs.append((adjustment.group_code.code, adjustment.reason_code.code))
                        #datum[f"adj_{index}_group"] = adjustment.group_code.code
                        #datum[f"adj_{index}_code"] = adjustment.reason_code.code
                        #datum[f"adj_{index}_amount"] = adjustment.amount
                    adjs = list(set(adjs))
                    for index, adjustment in enumerate(adjs):
                        datum[f"adj_{index}_group"] = adjustment[0]
                        datum[f"adj_{index}_code"] = adjustment[1]

                    for index, remark in enumerate(claim.remarks):
                        rems.append((remark.qualifier.code, remark.code.code))
                    rems = list(set(rems))
                    for index, remark in enumerate(rems):
                        datum[f"rem_{index}_qual"] = remark[0]
                        datum[f"rem_{index}_code"] = remark[1]

                    data.append(datum)

        df = pd.DataFrame(data)
        df["transmission_date"] = str(self.interchange.transmission_date)

        return df

    @staticmethod
    def serialize_claim(
        financial_information: FinancialInformationSegment,
        processed_date: DateSegment,
        organization: OrganizationLoop,
        #payee: OrganizationLoop,
        claim: ClaimLoop,
    ) -> dict:
        # if the service doesn't have a start date assume the service and claim dates match
        start_date = None
        start_date_type = None
        if claim.claim_statement_period_start:
            start_date = claim.claim_statement_period_start.date

        # if the service doesn't have an end date assume the service and claim dates match
        end_date = None
        end_date_type = None
        if claim.claim_statement_period_end:
            end_date = claim.claim_statement_period_end.date

        # get received and processed date if available
        if claim.claim_received_date:
            claim_received_date = claim.claim_received_date.date
        else:
            claim_received_date = None

        ea_code = None
        for reference in claim.references:
            if reference._qualifier.code == "EA":
                ea_code = reference.value

        # get facility_npi
        if len(claim.provider_summary) > 0:
            facility_npi = claim.provider_summary[0].value
        elif organization.payee.id_type == "XX":
            facility_npi = organization.payee.identification_code
        else:
            facility_npi = None

        datum = {
            "marker": claim.claim.marker,
            "patient_identifier": ea_code,
            "patient": claim.patient.name,
            "id_code_qualifier": claim.patient.identification_code_qualifier,
            "id_code": claim.patient.identification_code,
            "code": None,
            "modifier": None,
            "qualifier": None,
            "allowed_units": None,
            "billed_units": None,
            "transaction_date": financial_information.transaction_date,
            "icn": claim.claim.icn,
            "charge_amount": claim.claim.charge_amount,
            "allowed_amount": None,
            "paid_amount": claim.claim.paid_amount,
            "payer": organization.payer.name,
            "start_date": None,
            "end_date": None,
            "claim_status_code": claim.claim.status.code,
            "claim_status_desc": claim.claim.status.description,
            "claim_facility_code": claim.claim.claim_facility_code,
            "claim_facility_desc": claim.claim.claim_facility_desc,
            "claim_freq_type": claim.claim.claim_freq_type,
            "claim_freq_desc": claim.claim.claim_freq_desc,
            "claim_start_date": start_date,
            "claim_end_date": end_date,
            "claim_received_date": claim_received_date,
            "claim_processed_date": processed_date.date,
            "rendering_provider": (
                claim.rendering_provider.name if claim.rendering_provider else None
            ),
            "payer_classification": str(claim.claim.status.payer_classification),
            "was_forwarded": claim.claim.status.was_forwarded,
            "facility_npi": facility_npi,
        }

        return datum

    @staticmethod
    def serialize_service(
        financial_information: FinancialInformationSegment,
        processed_date: DateSegment,
        #payer: OrganizationLoop,
        organization: OrganizationLoop,
        claim: ClaimLoop,
        service: ServiceLoop,
    ) -> dict:
        # if the service doesn't have a start date assume the service and claim dates match
        start_date = None
        claim_start_date = None
        if service.service_period_start:
            start_date = service.service_period_start.date
        if claim.claim_statement_period_start:
            claim_start_date = claim.claim_statement_period_start.date

        # if the service doesn't have an end date assume the service and claim dates match
        end_date = None
        claim_end_date = None
        if service.service_period_end:
            end_date = service.service_period_end.date
        if claim.claim_statement_period_end:
            claim_end_date = claim.claim_statement_period_end.date

        # get received and processed date if available
        if claim.claim_received_date:
            claim_received_date = claim.claim_received_date.date
        else:
            claim_received_date = None

        ea_code = None
        for reference in claim.references:
            if reference._qualifier.code == "EA":
                ea_code = reference.value

        # get facility_npi
        if len(claim.provider_summary) > 0:
            facility_npi = claim.provider_summary[0].value
        elif organization.payee.id_type == "XX":
            facility_npi = organization.payee.identification_code
        else:
            facility_npi = None

        datum = {
            "marker": claim.claim.marker,
            "patient_identifier": ea_code,
            "patient": claim.patient.name,
            "id_code_qualifier": claim.patient.identification_code_qualifier,
            "id_code": claim.patient.identification_code,
            "code": service.service.code,
            "modifier": service.service.modifier,
            "qualifier": service.service.qualifier,
            "allowed_units": service.service.allowed_units,
            "billed_units": service.service.billed_units,
            "transaction_date": financial_information.transaction_date,
            "icn": claim.claim.icn,
            "charge_amount": service.service.charge_amount,
            "allowed_amount": service.allowed_amount,
            "paid_amount": service.service.paid_amount,
            "payer": organization.payer.name,
            "service_start_date": start_date,
            "service_end_date": end_date,
            "claim_status_code": claim.claim.status.code,
            "claim_status_desc": claim.claim.status.description,
            "claim_facility_code": claim.claim.claim_facility_code,
            "claim_facility_desc": claim.claim.claim_facility_desc,
            "claim_freq_type": claim.claim.claim_freq_type,
            "claim_freq_desc": claim.claim.claim_freq_desc,
            "claim_start_date": claim_start_date,
            "claim_end_date": claim_end_date,
            "claim_received_date": claim_received_date,
            "claim_processed_date": processed_date.date if processed_date else None,
            "rendering_provider": (
                claim.rendering_provider.name if claim.rendering_provider else None
            ),
            "payer_classification": str(claim.claim.status.payer_classification),
            "was_forwarded": claim.claim.status.was_forwarded,
            "facility_npi": facility_npi,
        }

        return datum

    @classmethod
    def build(cls, file_path: str) -> "TransactionSet":
        interchange = None
        financial_information = None
        claims = []
        organizations = []

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
        processed_date = None

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

            if response.key == "processed date":
                processed_date = response.value

            if response.key == "organization":
                organizations.append(response.value)

            if response.key == "claim":
                claims.append(response.value)

        return TransactionSet(
            interchange, financial_information, processed_date, claims, organizations, file_path
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

        if identifier == DateSegment.identification:
            processed_date = DateSegment(segment)
            if processed_date.qualifier == "processed":
                return BuildAttributeResponse(
                    "processed date", processed_date, None, segments
                )

        if identifier == OrganizationLoop.initiating_identifier:
            organization, segments, segment = OrganizationLoop.build(segment, segments)
            return BuildAttributeResponse(
                "organization", organization, segment, segments
            )

        elif identifier == ClaimLoop.initiating_identifier:
            claim, segments, segment = ClaimLoop.build(segment, segments)
            return BuildAttributeResponse("claim", claim, segment, segments)

        else:
            return BuildAttributeResponse(None, None, None, segments)


if __name__ == "__main__":
    pass
