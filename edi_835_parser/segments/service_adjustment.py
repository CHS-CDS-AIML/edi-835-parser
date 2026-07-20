from edi_835_parser.elements.identifier import Identifier
from edi_835_parser.elements.dollars import Dollars
from edi_835_parser.elements.adjustment_group_code import AdjustmentGroupCode
from edi_835_parser.elements.adjustment_reason_code import AdjustmentReasonCode
from edi_835_parser.segments.utilities import split_segment

class AdjustmentDetail:
    """Represents a single CARC triplet breakdown."""
    group_code = AdjustmentGroupCode()
    reason_code = AdjustmentReasonCode()
    amount = Dollars()

    def __init__(self, group_code: str, reason_code: str, amount: float):
        self.group_code = group_code
        self.reason_code = reason_code
        self.amount = amount 

    def __repr__(self):
        return f"ServiceAdjustment(Group: {self.group_code}, CARC: {self.reason_code}, Amount: {self.amount})"

class ServiceAdjustment:
    identification = "CAS"

    identifier = Identifier()
    def __init__(self, segment: str):
        self.segment = segment
        segment = split_segment(segment)

        # get adjustment list
        self.adjustments = []

        # get the identifier (should be 'CAS')
        self.identifier = segment[0]
        # get the group code
        base_group_code = segment[1]

        # check how many CARC elements
        n_ele = len(segment)

        for i in range(2, n_ele, 3):
            # get reason code and amount
            reason_code = segment[i]
            amount = segment[i+1]

            # set AdjustmentDetail
            carc = AdjustmentDetail(
                    group_code=base_group_code,
                    reason_code=reason_code,
                    amount=amount,
                    )

            self.adjustments.append(carc)

    def __repr__(self):
        return "\n".join(str(item) for item in self.__dict__.items())


if __name__ == "__main__":
    pass
