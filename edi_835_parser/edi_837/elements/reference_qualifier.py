from edi_835_parser.elements import Element, Code

# https://ushik.ahrq.gov/ViewItemDetails?&system=sdo&itemKey=133213000
reference_qualifiers = {
    "G1": "authorization_number",
    "82": "rendering_provider",
    "77": "location",
}


class ReferenceQualifier(Element):

    def parser(self, value: str) -> Code:
        description = reference_qualifiers.get(value, None)
        return Code(value, description)
