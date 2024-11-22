from edi_835_parser.elements import Element, Code
from typing import Iterator, Tuple, Optional, List

# import List
diagnosis_codes = {"HI": "diagnosis codes"}


class DiagnosisCodes(Element):
    def parser(self, value: str) -> List[Code]:
        splits = value.split()
        codes = list()
        for code_str in splits:
            description = code_str.split(":")[0]
            element = code_str.split(":")[1]
            codes.append(Code(element, description))
        return codes
