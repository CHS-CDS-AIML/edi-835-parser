from edi_835_parser.elements import Element, Code

# import List
remark_qualifiers = {"HI": "diagnosis codes"}


class RemarkQualifier(Element):
    def parser(self, value: str) -> List[Code]:
        splits = value.split()
        codes = list()
        for code_str in splits:
            description = code_str.split(":")[0]
            element = code_str.split(":")[1]
            codes.append(Code(element, description))
        return codes
