# created by Barry at 2022.6.15
from typing import Optional

from ..globals import xsi


class Physical_Vehicle_Link_Ref:
    def __init__(self,
                 id_ref,
                 docref=None,
                 doctype=None):
        self.id_ref = id_ref
        self.docref = docref
        self.doctype = doctype


def read_physical_vehicle_link_ref(et_element):
    id_ref = et_element.get("ID-REF") if et_element.get("ID-REF") is not None else None
    docref = et_element.get("DOCREF") if et_element.get("DOCTYPE") is not None else None
    doctype = et_element.get("DOCTYPE") if et_element.get("DOCTYPE") is not None else None
    return Physical_Vehicle_Link_Ref(id_ref, docref, doctype)


class Functional_Group_Ref:
    def __init__(self,
                 id_ref,
                 docref,
                 doctype):
        self.id_ref = id_ref
        self.docref = docref
        self.doctype = doctype


def read_functional_group_ref(et_element):
    id_ref = et_element.get("ID-REF") if et_element.get("ID-REF") is not None else None
    docref = et_element.get("DOCREF") if et_element.get("DOCTYPE") is not None else None
    doctype = et_element.get("DOCTYPE") if et_element.get("DOCTYPE") is not None else None
    return Functional_Group_Ref(id_ref, docref, doctype)


class ECU_Proxy_Ref:
    def __init__(self, id_ref, docref, doctype):
        self.id_ref = id_ref
        self.docref = docref
        self.doctype = doctype


def read_ecu_proxy_ref(et_element):
    id_ref = et_element.get("ID-REF") if et_element.get("ID-REF") is not None else None
    docref = et_element.get("DOCREF") if et_element.get("DOCTYPE") is not None else None
    doctype = et_element.get("DOCTYPE") if et_element.get("DOCTYPE") is not None else None
    return ECU_Proxy_Ref(id_ref, docref, doctype)


class Protocol_Ref:
    def __init__(self, id_ref, docref, doctype):
        self.id_ref = id_ref
        self.docref = docref
        self.doctype = doctype


def read_protocol_ref(et_element):
    id_ref = et_element.get("ID-REF") if et_element.get("ID-REF") is not None else None
    docref = et_element.get("DOCREF") if et_element.get("DOCTYPE") is not None else None
    doctype = et_element.get("DOCTYPE") if et_element.get("DOCTYPE") is not None else None
    return Protocol_Ref(id_ref, docref, doctype)


class Base_Variant_Ref:
    def __init__(self, id_ref, docref, doctype):
        self.id_ref = id_ref
        self.docref = docref
        self.doctype = doctype


def read_base_variant_ref(et_element):
    id_ref = et_element.get("ID-REF") if et_element.get("ID-REF") is not None else None
    docref = et_element.get("DOCREF") if et_element.get("DOCTYPE") is not None else None
    doctype = et_element.get("DOCTYPE") if et_element.get("DOCTYPE") is not None else None
    return Base_Variant_Ref(id_ref, docref, doctype)


class Logical_Link:
    def __init__(self,
                 id,
                 oid,
                 type,
                 short_name,
                 long_name,
                 physical_vehicle_link_ref: Optional[Physical_Vehicle_Link_Ref] = None,
                 ecu_proxy_ref: Optional[ECU_Proxy_Ref] = None,
                 functional_group_ref: Optional[Functional_Group_Ref] = None,
                 base_variant_ref: Optional[Base_Variant_Ref] = None,
                 protocol_ref: Optional[Protocol_Ref] = None,
                 prot_stack_snref: Optional[str] = None
                 ):
        self.id = id
        self.oid = oid
        self.type = type
        self.short_name = short_name
        self.long_name = long_name
        self.physical_vehicle_link_ref = physical_vehicle_link_ref
        self.ecu_proxy_ref = ecu_proxy_ref
        self.functional_group_ref = functional_group_ref
        self.base_variant_ref = base_variant_ref
        self.protocol_ref = protocol_ref
        self.prot_stack_snref = prot_stack_snref


def read_logical_link_from_odx(et_element):
    id = et_element.get("ID")
    oid = et_element.get("OID")
    type = et_element.get(f"{xsi}type")
    short_name = et_element.find("SHORT-NAME").text
    long_name = et_element.find("LONG-NAME").text
    physical_vehicle_link_ref = read_physical_vehicle_link_ref(et_element.find("PHYSICAL-VEHICLE-LINK-REF")) \
        if et_element.find("PHYSICAL-VEHICLE-LINK-REF") is not None else None
    ecu_proxy_ref = read_ecu_proxy_ref(et_element.find("ECU-PROXY-REF")) \
        if et_element.find("ECU-PROXY-REF") is not None else None
    functional_group_ref = read_functional_group_ref(et_element.find("FUNCTIONAL-GROUP-REF")) \
        if et_element.find("FUNCTIONAL-GROUP-REF") is not None else None
    base_variant_ref = read_base_variant_ref(et_element.find("BASE-VARIANT-REF")) \
        if et_element.find("BASE-VARIANT-REF") is not None else None
    protocol_ref = read_protocol_ref(et_element.find("PROTOCOL-REF")) \
        if et_element.find("PROTOCOL-REF") is not None else None
    prot_stack_snref = et_element.find("PROT-STACK-SNREF").get("SHORT-NAME") \
        if et_element.find("PROT-STACK-SNREF") is not None else None
    return Logical_Link(id,
                        oid,
                        type,
                        short_name,
                        long_name,
                        physical_vehicle_link_ref,
                        ecu_proxy_ref,
                        functional_group_ref,
                        base_variant_ref,
                        protocol_ref,
                        prot_stack_snref)
