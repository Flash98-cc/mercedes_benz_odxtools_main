# created by Barry at 2022.6.21
#  p253 figure 157
from dataclasses import dataclass
from ..globals import xsi
from ..odxtypes import DataType
from ..utils import read_description_from_odx


@dataclass()
class Phys_Segment:
    id: str = None
    oid: str = None
    type: str = None
    short_name: str = None
    long_name: str = None
    description: str = None
    # fillbyte's type is hexBinary, FILLBYTE describles the byte for filling empty areas to
    # complete the physical segnents
    fillbyte: DataType.A_BYTEFIELD = None
    # block size can be used by the flash job to enable parallel programming of memory sub-units to
    # increase in the performanceof the flash process
    block_size: int = None
    # describles the first valid address of segment
    start_address: DataType.A_BYTEFIELD = None
    # defines the last valid address of that belongs to the current segment
    end_address: DataType.A_BYTEFIELD = None
    # size can be used as alternative to END-ADDRESS, it defines the size of the segment in bytes
    size: int = 0


def read_phys_segment_from_phys_mem(et_element):
    if et_element is None:
        return None

    id = et_element.get("ID")
    oid = et_element.get("OID") if et_element.get("OID") is not None else None
    short_name = et_element.find("SHORT-NAME").text if et_element.find("SHORT-NAME") is not None else None
    long_name = et_element.find("LONG-NAME").text if et_element.find("LONG-NAME") is not None else None
    description = read_description_from_odx(et_element.find("DESC"))
    fillbyte = et_element.find("FILLBYTE").text if et_element.find("FILLBYTE") is not None else None
    block_size = et_element.find("BLOCK-SIZE").text if et_element.find("BLOCK-SIZE") is not None else None
    start_address = et_element.find("START-ADDRESS").text

    type = et_element.find(f"{xsi}type")
    if type == "ADDRDEF-PHYS-SEGMENT":
        end_address = et_element.find("ADDRDEF-PHYS-SEGMENT").text
        return Phys_Segment(id,
                            oid,
                            short_name,
                            long_name,
                            description,
                            fillbyte,
                            block_size,
                            start_address,
                            end_address=end_address)
    elif type == "SIZEDEF-PHYS-SEGMENT":
        size = et_element.find("SIZE").text
        return Phys_Segment(id,
                            oid,
                            type,
                            short_name,
                            long_name,
                            description,
                            fillbyte,
                            block_size,
                            start_address,
                            size=size
                            )
