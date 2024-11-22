from edi_835_parser.edi_837.elements.diagnosis_codes import DiagnosisCodes as DiagnosisCodesElement
from edi_835_parser.edi_837.elements.diagnosis_codes_type import DiagnosisCodesType
from edi_835_parser.elements.identifier import Identifier
from edi_835_parser.segments.utilities import split_segment

class DiagnosisCodes:
    identification = "HI"

    identifier = Identifier()
    diagnosis_codes = DiagnosisCodesElement()
    type = DiagnosisCodesType()

    def __init__(self, segment: str):
        self.segment = segment
        segment = split_segment(segment)

        self.identifier = segment[0]
        self.diagnosis_codes = segment[1]

    def __repr__(self):
        return "\n".join(str(item) for item in self.__dict__.items())


if __name__ == "__main__":
    pass
