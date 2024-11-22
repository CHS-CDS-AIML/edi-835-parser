from edi_835_parser.elements import Element

# https://www.stedi.com/edi/x12/element/1032
provider_types = {
}


class DiagnosisCodesType(Element):

    def parser(self, value: str) -> str:
        return diagnosis_codes_types.get(value, value)
