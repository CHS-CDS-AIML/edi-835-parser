from edi_835_parser.elements import Element, Code

type_of_facility = {
    1: "hospital",
    2: "skilled nursing facility",
    3: "home health",
    4: "religious nonmedical health care institutions",
    6: "intermediate care",
    7: "clinic",
    8: "special facility",
    9: "reserved for national assignemnt",
}

bill_classification = {
    1: "inpatient (part A)",
    2: "inpatient (part B)",
    3: "outpatient",
    4: "other",
    5: "intermediate care level 1",
    6: "intermediate care level 2",
    7: "subacute inpatient",
    8: "NA",
}

class ClaimFacility:
    def parser(self, value: str) -> Code:
        tof_value = int(value[0])
        bc_value = int(value[1])

        tof_description = type_of_facility.get(tof_value, None)
        bc_description = bill_classification.get(bc_value, None)

        final_value = int(str(tof_value) + str(bc_value))
        final_description = f"{bc_description}, {tof_description}"

        return Code(final_value, final_description)
