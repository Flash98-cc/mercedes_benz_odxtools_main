# created by Barry at 2022.6.15

from .vehicle_connector import Vehicle_Connector, read_vehicle_connector_from_odx
from .logical_link import Logical_Link, read_logical_link_from_odx
from .physical_vehicle_link import Physical_Vehicle_Link, read_physical_vehicle_link_from_odx


class Vehicle_Information:
    def __init__(self,
                 oid,
                 short_name=None,
                 long_name=None,
                 info_component_refs: list[str] = None,
                 vehicle_connectors: list[Vehicle_Connector] = None,
                 logical_links: list[Logical_Link] = None,
                 physical_vehicle_links: list[Physical_Vehicle_Link] = None
                 ):
        self.oid = oid
        self.short_name = short_name
        self.long_name = long_name
        self.info_component_refs = info_component_refs
        self.vehicle_connectors = vehicle_connectors
        self.logical_links = logical_links
        self.physical_vehicle_links = physical_vehicle_links


def read_vehicle_information_from_odx(et_element):
    oid = et_element.get("OID")
    short_name = et_element.find("SHORT-NAME").text if et_element.find("SHORT-NAME") is not None else None
    long_name = et_element.find("LONG-NAME").text if et_element.find("LONG-NAME") is not None else None
    info_component_refs = []
    for info_component_ref in et_element.iterfind("INFO-COMPONENT-REF"):
        info_component_refs.append(info_component_ref.get("ID-REF"))
        print(info_component_ref.get("ID-REF"))

    vehicle_connectors = [read_vehicle_connector_from_odx(el)
                          for el in et_element.iterfind("VEHICLE-CONNECTORS/VEHICLE-CONNECTOR")]

    logical_links = [read_logical_link_from_odx(el)
                     for el in et_element.iterfind("LOGICAL-LINKS/LOGICAL-LINK")]

    physical_vehicle_links = [read_physical_vehicle_link_from_odx(el)
                              for el in et_element.iterfind("PHYSICAL-VEHICLE-LINKS/PHYSICAL-VEHICLE-LINK")]

    return Vehicle_Information(oid, short_name, long_name, info_component_refs,
                               vehicle_connectors, logical_links, physical_vehicle_links)
