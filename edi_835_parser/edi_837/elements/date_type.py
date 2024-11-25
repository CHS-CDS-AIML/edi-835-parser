from edi_835_parser.elements import Element

# https://www.stedi.com/edi/x12/element/1032
date_types = {
        "098": "discharged",
        "296": "disabled_to",
        "297": "disabled_from",
        "304": "last_seen",
        "435": "admission_from",
        "454": "initial_treatment",
}


class DateType(Element):

    def parser(self, value: str) -> str:
        return subscriber_types.get(value, value)
