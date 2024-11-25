from edi_835_parser.elements import Element

# https://ediacademy.com/blog/x12-n101-entity-identifier-codes/
date_codes = {
        "098": "discharged",
        "296": "disabled_to",
        "297": "disabled_from",
        "304": "last_seen",
        "435": "admission_from",
        "454": "initial_treatment",
}


class DateCode(Element):

	def parser(self, value: str) -> str:
		return dates_codes.get(value, value)
