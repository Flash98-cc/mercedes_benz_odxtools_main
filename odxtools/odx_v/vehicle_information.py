# created by Barry at 2022.6.15

from .vehicle_connector import Vehicle_Connector, read_vehicle_connector_from_odx
from .logical_link import Logical_Link, read_logical_link_from_odx
from .physical_vehicle_link import Physical_Vehicle_Link, read_physical_vehicle_link_from_odx
from .info_component import Info_Component
from .ecu_group import Ecu_Group, read_ecu_group_from_odx

from dataclasses import dataclass, field


@dataclass()
class Info_Component_Ref:
    id_ref: str = None
    doctype: str = None
    docref: str = None
    info_component: Info_Component = None

    def _resolve_references(self, id_lookup):
        pass


def read_info_component_ref_from_odx(et_element):
    id_ref = et_element.get("ID-REF")
    doctype = et_element.get("DOCTYPE")
    docref = et_element.get("DOCREF")
    return Info_Component_Ref(id_ref, doctype, docref)


class Vehicle_Information:
    def __init__(self,
                 oid,
                 short_name=None,
                 long_name=None,
                 info_component_refs=None,
                 vehicle_connectors: list[Vehicle_Connector] = None,
                 logical_links: list[Logical_Link] = None,
                 physical_vehicle_links: list[Physical_Vehicle_Link] = None
                 ):

        if info_component_refs is None:
            info_component_refs = [Info_Component_Ref]
        self.oid = oid
        self.short_name = short_name
        self.long_name = long_name
        self.vehicle_connectors = vehicle_connectors
        self.logical_links = logical_links
        self.physical_vehicle_links = physical_vehicle_links
        self.info_component_refs = info_component_refs

    # Because the protocol、functional-group、base-variant have update information in id-lookup
    def _build_id_lookup(self, id_lookup):
        pass

    def _resolve_references(self, id_lookup):
        pass


def read_vehicle_information_from_odx(et_element):
    oid = et_element.get("OID")
    short_name = et_element.find("SHORT-NAME").text if et_element.find("SHORT-NAME") is not None else None
    long_name = et_element.find("LONG-NAME").text if et_element.find("LONG-NAME") is not None else None

    info_component_refs = [read_info_component_ref_from_odx(el)
                           for el in et_element.iterfind("INFO-COMPONENT-REFS/INFO-COMPONENT-REF")]

    vehicle_connectors = [read_vehicle_connector_from_odx(el)
                          for el in et_element.iterfind("VEHICLE-CONNECTORS/VEHICLE-CONNECTOR")]

    logical_links = [read_logical_link_from_odx(el)
                     for el in et_element.iterfind("LOGICAL-LINKS/LOGICAL-LINK")]

    physical_vehicle_links = [read_physical_vehicle_link_from_odx(el)
                              for el in et_element.iterfind("PHYSICAL-VEHICLE-LINKS/PHYSICAL-VEHICLE-LINK")]

    # TODO: ECU-GROUP is not used for now
    ecu_groups = [read_ecu_group_from_odx(el)
                  for el in et_element.iterfind("ECU-GROUPS/ECU-GROUP")]

    return Vehicle_Information(oid, short_name, long_name, info_component_refs,
                               vehicle_connectors, logical_links, physical_vehicle_links)
