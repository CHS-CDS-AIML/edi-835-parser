from edi_835_parser.elements import Element

# https://ediacademy.com/blog/x12-n101-entity-identifier-codes/
entity_codes = {
	'IL': 'patient',
}


class EntityCode(Element):

	def parser(self, value: str) -> str:
		return entity_codes.get(value, value)
