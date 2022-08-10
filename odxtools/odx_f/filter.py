# created by Barry at 2022.06.22

from dataclasses import dataclass

from ..globals import xsi
from ..odxtypes import DataType
from ..globals import xsi


# Filter can be used to reduce the flash data from the source
# Filter xml struct  can be found in P240 ISO-22901-1
class Filter:
    def __init__(self,
                 type: str,
                 filter_start: DataType.A_BYTEFIELD,
                 filter_end: DataType.A_BYTEFIELD,
                 filter_size: int):
        # judge type value
        assert type in ["SIZEDEF-FILTER", "ADDRDEF-FILTER"], "type must be SIZEDEF-FILTER or ADDRDEF-FILTER"
        self.type = type
        self.filter_start = filter_start
        if self.type == "SIZEDEF-FILTER":
            self.filter_size = filter_size
        elif self.type == "ADDRDEF-FILTER":
            self.filter_end = filter_end
# TODO: filter_size = filter_start - filter_end


def read_filter_from_datablock(et_element):
    if et_element is None:
        return None
    type = et_element.get(f"{xsi}type")
    filter_start = et_element.find("FILTER-START").text
    filter_end = et_element.find("FILTER-END").text if et_element.find("FILTER-END") is not None else None
    filter_size = et_element.find("FILTER-SIZE").text if et_element.find("FILTER-START") is not None else None
    return Filter(type, filter_start, filter_end, filter_size)
