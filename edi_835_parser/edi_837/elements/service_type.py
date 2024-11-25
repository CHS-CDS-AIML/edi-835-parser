from edi_835_parser.elements import Element

# https://www.stedi.com/edi/x12/element/1032
service_types = {
}


class ServiceType(Element):

    def parser(self, value: str) -> str:
        return service_types.get(value, value)
