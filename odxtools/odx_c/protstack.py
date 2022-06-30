# created by Barry at 2022/5/31 
from typing import Optional
from .comparam_subset_ref import Comparam_subset_ref, read_comparam_subset_ref_from_odx
from ..nameditemlist import NamedItemList
from ..utils import read_description_from_odx
from dataclasses import dataclass

# TODO protstack snref how to solve it


class ProtStack:
    def __init__(self,
                 id,
                 short_name,
                 long_name=None,
                 description=None,
                 pdu_protocol_type=None,
                 physical_link_type=None,
                 comparam_subset_refs=[]):
        self.id = id
        self.short_name = short_name
        self.long_name = long_name
        self.description = description
        self.pdu_protocol_type = pdu_protocol_type
        self.physical_link_type = physical_link_type
        self.comparam_subset_refs = comparam_subset_refs


def read_prot_stack_from_odx(et_element, enable_candela_workarounds=True):
    id = et_element.get("ID")
    short_name = et_element.find("SHORT-NAME").text
    long_name = et_element.find("LONG-NAME").text

    description = None
    if et_element.find("DESC") is not None:
        description = read_description_from_odx(et_element.find("DESC"))

    pdu_protocol_type = et_element.find("PDU-PROTOCOL-TYPE").text
    physical_link_type = et_element.find("PHYSICAL-LINK-TYPE").text
    comparam_subset_refs = [read_comparam_subset_ref_from_odx(dl_element)
                            for dl_element in et_element.iterfind("COMPARAM-SUBSET-REFS/COMPARAM-SUBSET-REF")]
    return ProtStack(id,
                     short_name,
                     long_name=long_name,
                     description=description,
                     pdu_protocol_type=pdu_protocol_type,
                     physical_link_type=physical_link_type,
                     comparam_subset_refs=comparam_subset_refs
                     )


@dataclass()
class Prot_Stack_Snref:
    snref: str = None
    prot_stack: ProtStack = None


def read_prot_stack_snref(et_element):
    if et_element is None:
        return None
    snref = et_element.get("SHORT-NAME")
    return Prot_Stack_Snref(snref)

