# created by Barry at 2022.6.15
from ..globals import xsi


# TODO info-component's MATCHING-COMPONENT has not parsed yet
class Info_Component:
    def __init__(self,
                 id,
                 oid,
                 type,
                 short_name,
                 long_name):
        self.id = id
        self.oid = oid
        self.type = type
        self.short_name = short_name
        self.long_name = long_name


def read_info_component_from_odx(et_elemnet):
    id = et_elemnet.get("ID")
    oid = et_elemnet.get("OID")
    type = et_elemnet.get(f"{xsi}type")
    short_name = et_elemnet.find("SHORT-NAME").text
    long_name = et_elemnet.find("LONG-NAME").text
    return Info_Component(id,
                          oid,
                          type,
                          short_name,
                          long_name)