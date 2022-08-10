# created by Barry at 2022.6.15
from enum import Enum
from typing import Optional


class PIN_TYPE(Enum):
    SINGLE = "SINGLE"


class Vehicle_Connector_Pin:
    def __init__(self,
                 id,
                 oid,
                 short_name,
                 long_name,
                 pin_number,
                 type: Optional[PIN_TYPE] = None,
                 ):
        self.id = id
        self.oid = oid
        self.type = type
        self.short_name = short_name
        self.long_name = long_name
        self.pin_number = pin_number


def read_vehicle_connector_pin_from_odx(et_element):
    id = et_element.get("ID")
    oid = et_element.get("OID")

    type = None
    pintype = et_element.get("TYPE") if et_element.get("TYPE") is not None else None
    for Pin_type in PIN_TYPE:
        if Pin_type.value == pintype:
            type = Pin_type
        else:
            type = None

    short_name = et_element.find("SHORT-NAME").text if et_element.find("SHORT-NAME") is not None else None
    long_name = et_element.find("LONG-NAME").text if et_element.find("LONG-NAME") is not None else None
    pin_number = et_element.find("PIN-NUMBER").text

    return Vehicle_Connector_Pin(id, oid, short_name, long_name, pin_number, type)
