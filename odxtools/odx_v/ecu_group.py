# created by Barry at 2022.06.21

from dataclasses import dataclass


@dataclass()
class Ecu_Group:
    oid: str = None
    short_name: str = None
    long_name: str = None
    desc: str = None

    # TODO: how to define GROUP-MEMBER


def read_ecu_group_from_odx(et_element):
    oid = et_element.get("OID")
    short_name = et_element.find("SHORT-NAME") if et_element.find("SHORT-NAME") is not None else None
    long_name = et_element.find("SHORT-NAME") if et_element.find("LONG-NAME") is not None else None
    desc = et_element.find("DESCRIPTION") if et_element.find("DESC") is not None else None

