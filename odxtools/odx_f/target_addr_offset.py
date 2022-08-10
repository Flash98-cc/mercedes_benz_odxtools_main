# created by Barry at 2022.06.22
from ..odxtypes import DataType
from ..globals import xsi


class Target_Addr_Offset:
    def __init__(self,
                 type: str = None,
                 positive_offset: DataType.A_BYTEFIELD = None,
                 negative_offset: DataType.A_BYTEFIELD = None
                 ):
        assert type in ["POS-OFFSET", "NEG-OFFSET"], "TYPE must be POS-OFFSET OR NEG-OFFSET"
        self.type = type
        if type == "POS-OFFSET":
            self.positive_offset = positive_offset
        elif type == "NEG-OFFSET":
            self.negative_offset = negative_offset


def read_target_addr_offset(et_element):
    if et_element is None:
        return None
    type = et_element.get(f"{xsi}TYPE")
    if type == "POS-OFFSET":
        positive_offset = et_element.find("POS-OFFSET").text
        return Target_Addr_Offset(type,
                                  positive_offset=positive_offset)
    elif type == "NEG-OFFSET":
        negative_offset = et_element.find("NEG-OFFSET").text
        return Target_Addr_Offset(type,
                                  negative_offset=negative_offset)
