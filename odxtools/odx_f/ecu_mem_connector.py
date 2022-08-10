# created by Barry at 2022.06.21
# see p254 7.5.3 ECU-MEM-CONNECTOR data model description
from dataclasses import dataclass

from ..utils import read_description_from_odx
from ..admindata import AdminData, read_admin_data_from_odx
from ..diaglayer import DiagLayer, read_short_name, read_long_name
from .ecu_mem import Ecu_Mem
from .flash_class import Flash_Class, read_flash_class
from .session_desc import Session_Desc, read_session_desc
from .ident_desc import Ident_Desc, read_ident_desc


@dataclass()
class Ecu_Mem_Ref:
    id_ref: str = None
    ecu_mem: Ecu_Mem = None


def read_ecu_mem_ref(et_element):
    if et_element is None:
        return None
    id_ref = et_element.get("ID-REF")
    return Ecu_Mem_Ref(id_ref)


@dataclass()
class Ecu_Variant_Ref:
    id_ref: str = None
    ecu_variant: DiagLayer = None


def read_ecu_variant_ref(et_element):
    if et_element is None:
        return None
    id_ref = et_element.get("ID-REF")
    return Ecu_Variant_Ref(id_ref)


@dataclass()
class Base_Variant_Ref:
    id_ref: str = None
    base_variant: DiagLayer = None


def read_base_variant_ref(et_element):
    if et_element is None:
        return None
    id_ref = et_element.get("ID-REF")
    return Base_Variant_Ref(id_ref)


# layer store ECU-VARIANT AND BASE-VARIANT
@dataclass()
class Layer_Ref:
    id_ref: str = None
    type: str = None
    layer: DiagLayer = None


def read_layer_ref(et_element):
    if et_element is None:
        return None
    id_ref = et_element.get("ID-REF")
    return Layer_Ref(id_ref)


# ECU-MEM-CONNECTOR is used to connect the ECU-MEM to the diag-layer, also links the ECU-MEM-OBJECTS with DIAG-COMMS
@dataclass()
class Ecu_Mem_Connector:
    id: str = None
    oid: str = None
    short_name: str = None
    long_name: str = None
    description: str = None
    ecu_mem_ref: Ecu_Mem_Ref = None

    admin_data: AdminData = None
    flash_classs: list[Flash_Class] = None
    session_descs: list[Session_Desc] = None
    ident_descs: list[Ident_Desc] = None
    layer_refs: list[Layer_Ref] = None

    ecu_variant_refs: list[Ecu_Variant_Ref] = None
    base_variant_refs: list[Base_Variant_Ref] = None

    def _build_id_lookup(self, id_lookup):
        pass

    def _resolve_references(self, id_lookup):
        pass


def read_ecu_mem_connector_from_odx(et_element):
    if et_element is None:
        return None

    id = et_element.get("ID")
    oid = et_element.get("OID") if et_element.get("OID") is not None else None
    # short_name = read_short_name(et_element.find("SHORT-NAME"))
    short_name = et_element.find("SHORT-NAME").text
    long_name = read_long_name(et_element.find("LONG-NAME"))
    description = read_description_from_odx(et_element.find("DESC"))
    ecu_mem_ref = read_ecu_mem_ref(et_element.find("ECU-MEM-REF"))
    admin_data = read_admin_data_from_odx(et_element.find("ADMIN-DATA"))

    flash_classs = [read_flash_class(el)
                    for el in et_element.iterfind("FLASH-CLASSS/FLASH-CLASS")]

    session_descs = [read_session_desc(el)
                     for el in et_element.iterfind("SESSION-DESCS/SESSION-DESC")]

    ident_descs = [read_ident_desc(el)
                   for el in et_element.iterfind("IDENT-DESCS/IDENT-DESC")]

    layer_refs = [read_layer_ref(el)
                  for el in et_element.iterfind("LAYER-REFS/LAYER-REF")]

    return Ecu_Mem_Connector(id,
                             oid,
                             short_name,
                             long_name,
                             description,
                             ecu_mem_ref,
                             admin_data,
                             flash_classs,
                             session_descs,
                             ident_descs,
                             layer_refs)
