from edi_835_parser.elements import Element

# https://www.stedi.com/edi/x12/element/1032
subscriber_types = {
}


class SubscriberType(Element):

    def parser(self, value: str) -> str:
        return subscriber_types.get(value, value)
