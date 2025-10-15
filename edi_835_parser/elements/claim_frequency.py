from edi_835_parser.elements import Element, Code

# https://resdac.org/cms-data/variables/claim-frequency-code-ffs
claim_frequency_codes = {
	'0': 'non-payment/zero claims',
    '1': 'admit thru discharge claim',
    '2': 'interim - first claim',
    '3': 'interim - continuing claim',
    '4': 'interim - last claim',
    '5': 'late charge(s) only claim',
    '7': 'Replacement of prior claim',
    '8': 'void/cancel prior claim',
    '9': 'final claim',
    'G': 'common working file generated adjustment claim',
    'H': 'CMS generated adjustment claim',
    'I': 'misc. adjustment claim',
    'J': 'other adjustment request',
    'K': 'OIG Initiated Adjustment Claim',
    'M': 'medicare secondary payer adjustment',
    'P': 'adjustment required by QIO',
    'Q': 'claim submitted for reconsideration outside of timely limits',
    'Y': 'replacement of prior abbreviated encounter submission',
}


class ClaimFrequencyCode(Element):

	def parser(self, value: str) -> Code:
		description = claim_frequency_codes.get(value, None)
		return Code(value, description)
