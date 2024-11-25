from edi_835_parser.elements import Element

# https://www.stedi.com/edi/x12/element/1032
provider_types = {
}


class ProviderType(Element):

    def parser(self, value: str) -> str:
        return provider_types.get(value, value)
