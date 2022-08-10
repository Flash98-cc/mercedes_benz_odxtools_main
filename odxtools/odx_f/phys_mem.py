# created by Barry at 2022.06.21
# see p7.5.2.5 for more details
from dataclasses import dataclass
from typing import Optional

from .phys_segment import Phys_Segment, read_phys_segment_from_phys_mem
from ..utils import read_description_from_odx


# PHYS-MEM used to describle the physical memory layout of an ecu
@dataclass()
class Phys_Mem:
    id: str = None
    oid: str = None
    short_name: str = None
    long_name: str = None
    description: str = None
    phys_segments: list[Phys_Segment] = None


def read_phys_mem_from_odx(et_element):
    if et_element is None:
        return None

    id = et_element.get("ID")
    oid = et_element.get("OID") if et_element.find("OID") is not None else None
    short_name = et_element.find("SHORT-NAME").text if et_element.find("SHORT-NAME") is not None else None
    long_name = et_element.find("LONG-NAME").text if et_element.find("LONG-NAME") is not None else None
    description = read_description_from_odx(et_element.find("DESC"))
    phys_segments = [read_phys_segment_from_phys_mem(el)
                     for el in et_element.iterfind("PHYS-SEGMENTS/PHYS-SEGMENT")]

    return Phys_Mem(id,
                    oid,
                    short_name,
                    long_name,
                    description,
                    phys_segments)

