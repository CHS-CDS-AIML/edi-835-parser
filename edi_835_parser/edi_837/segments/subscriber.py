from edi_835_parser.elements.identifier import Identifier
from edi_835_parser.elements.subscriber_type import SubscriberType
from edi_835_parser.segments.utilities import split_segment


class Subscriber:
    """
    class representing subscriber segment
    """
    identification = "SBR"

    identifier = Identifier()
    type = SubscriberType()

    def __init__(self, segment: str):
        self.segment = segment
        segment = split_segment(segment)

        self.identifier = segment[0]
        self.responsibility = segment[1]# P = Primary, S = SEcondary, T = Tertiary
        self.relationship = segment[2 # Client relationship to insured, 01 = Spouse, 18 = self, 19 = child, G8 = other
        self.group_number = segment[3] # Policy/group number
        self.plan = segment[4] # Plan/Program
        self.msp = segment[5] # medicary secondary payer (msp) code

    def __repr__(self):
        return "\n".join(str(item) for item in self.__dict__.items())


if __name__ == "__main__":
    pass
