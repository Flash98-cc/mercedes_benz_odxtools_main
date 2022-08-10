# created by Barry at 2022.6.15

from .vehicle_connector_pin import Vehicle_Connector_Pin, read_vehicle_connector_pin_from_odx


class Vehicle_Connector:
    def __init__(self,
                 oid,
                 short_name,
                 long_name,
                 vehicle_connector_pins: list[Vehicle_Connector_Pin]):
        self.oid = oid
        self.short_name = short_name
        self.long_name = long_name
        self.vehicle_connector_pins = vehicle_connector_pins

    def _build_id_lookup(self, id_lookup):
        pass


def read_vehicle_connector_from_odx(et_element):
    oid = et_element.get("OID")
    short_name = et_element.find("SHORT-NAME").text
    long_name = et_element.find("LONG-NAME").text
    vehicle_connector_pins = [read_vehicle_connector_pin_from_odx(el)
                              for el in et_element.iterfind("VEHICLE-CONNECTOR-PINS/VEHICLE-CONNECTOR-PIN")]
    return Vehicle_Connector(oid,
                             short_name,
                             long_name,
                             vehicle_connector_pins)

