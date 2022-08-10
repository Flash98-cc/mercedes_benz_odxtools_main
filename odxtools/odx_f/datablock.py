# created by Barry at 2022.06.21
# see 7.5.2.3 for more details
from dataclasses import dataclass

from ..utils import read_description_from_odx
from ..audience import Audience, read_audience_from_odx
from .flashdata import Flashdata, read_flashdata_from_mem
from .filter import Filter, read_filter_from_datablock
from .segment import Segment, read_segment_from_datablock
from .own_ident import Own_Ident, read_own_ident
from .target_addr_offset import Target_Addr_Offset, read_target_addr_offset

from ..odxtypes import DataType

# TODO: filter_start, filter_end, source_start_addr, source_end_addr, pos_offset, neg_offset should be unsigned integer
#  in the hexadecimal format(32bit), and filter_size, uncompressed_size, compressed_size should be 32 bit unsigned
#  integer values in the decimal format


# datablock struct can be found in Figure 155
@dataclass()
class Flashdata_Ref:
    id_ref: str = None
    flashdata: Flashdata = None


def read_flashdata_ref(et_element):
    if et_element is None:
        return None
    id_ref = et_element.get("ID")
    return Flashdata_Ref(id_ref)


# describle the logical structure of the referenced FLASHDATA
@dataclass()
class Datablock:
    id: str = None
    oid: str = None
    short_name: str = None
    long_name: str = None
    description: str = None
    # type describes what kind of this datablock, this value will be used by a generic programming job to select the
    # method used to unlock or to program the flashdata in this datablock
    type: str = None
    audience: Audience = None
    flashdata_ref: Flashdata_Ref = None
    logical_block_index: DataType.A_BYTEFIELD = None
    # it can be used as a parameter for the service "erase memory"
    filters: list[Filter] = None
    segments: list[Segment] = None
    own_idents: list[Own_Ident] = None
    target_addr_offset: Target_Addr_Offset = None

    def _resolve_references(self, id_lookup):
        pass


def read_datablock_from_mem(et_element):
    if et_element is None:
        return None
    id = et_element.get("ID")
    oid = et_element.get("OID") if et_element.get("OID") is not None else None
    short_name = et_element.find("SHORT-NAME").text if et_element.find("SHORT-NAME") is not None else None
    long_name = et_element.find("LONG-NAME").text if et_element.find("LONG-NAME") is not None else None
    description = read_description_from_odx(et_element.find("DESC"))
    type = et_element.get("TYPE") if et_element.get("TYPE") is not None else None
    audience = read_audience_from_odx(et_element.find("AUDIENCE"))
    flashdata_ref = read_flashdata_ref(et_element.find("FLASHDATA-REF"))
    logical_block_index = et_element.find("LOGICAL-BLOCK-INDEX").text \
        if et_element.find("LOGICAL-BLOCK-INDEX") is not None else None

    filters = [read_filter_from_datablock(el)
               for el in et_element.iterfind("FILTERS/FILTER")]
    segments = [read_segment_from_datablock(el)
                for el in et_element.iterfind("SEGMENTS/SEGMENT")]
    own_idents = [read_own_ident(el)
                  for el in et_element.iterfind("OWN-IDENTS/OWN-IDENT")]
    target_addr_offset = read_target_addr_offset(et_element.find("TARGET-ADDR-OFFSET"))
    return Datablock(id,
                     oid,
                     short_name,
                     long_name,
                     description,
                     type,
                     audience,
                     flashdata_ref,
                     logical_block_index,
                     filters,
                     segments,
                     own_idents,
                     target_addr_offset
                     )

