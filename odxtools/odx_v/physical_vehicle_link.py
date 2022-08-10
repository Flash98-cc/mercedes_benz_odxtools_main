# created by Barry at 2022.6.15
from dataclasses import dataclass

from .vehicle_connector_pin import Vehicle_Connector_Pin


@dataclass()
class Vehicle_Connector_Pin_Ref:
    id_ref: str = None
    doctype: str = None
    docref: str = None
    vehicle_connector_pin: Vehicle_Connector_Pin = None


def read_vehicle_connector_pin_ref(et_element):
    id_ref = et_element.get("ID-REF")
    doctype = et_element.get("DOCTYPE")
    docref = et_element.get("DOCREF")
    return Vehicle_Connector_Pin_Ref(id_ref,
                                     doctype,
                                     docref)

class Physical_Vehicle_Link:
    def __init__(self,
                 id,
                 oid,
                 type,
                 short_name,
                 long_name,
                 vehicle_connector_pin_refs):
        self.id = id
        self.oid = oid
        self.type = type
        self.short_name = short_name
        self.long_name = long_name
        self.vehicle_connector_pin_refs = vehicle_connector_pin_refs

    # TODO: where to use this function
    def _resolve_references(self, id_lookup):
        pass


def read_physical_vehicle_link_from_odx(et_element):
    id = et_element.get("ID")
    oid = et_element.get("OID") if et_element.get("OID") is not None else None
    type = et_element.get("TYPE") if et_element.get("TYPE") is not None else None
    short_name = et_element.find("SHORT-NAME").text if et_element.find("SHORT-NAME") is not None else None
    long_name = et_element.find("LONG-NAME").text if et_element.find("LONG-NAME") is not None else None

    # vehicle_connector_pin_refs = []
    # for el in et_element.iterfind("VEHICLE-CONNECTOR-PIN-REFS/VEHICLE-CONNECTOR-PIN-REF"):
    #     vehicle_connector_pin_refs.append(el.get("ID-REF"))

    vehicle_connector_pin_refs = [read_vehicle_connector_pin_ref(el)
                                  for el in et_element.iterfind("VEHICLE-CONNECTOR-PIN-REFS/VEHICLE-CONNECTOR-PIN-REF")]

    return Physical_Vehicle_Link(id, oid, type, short_name, long_name, vehicle_connector_pin_refs)

