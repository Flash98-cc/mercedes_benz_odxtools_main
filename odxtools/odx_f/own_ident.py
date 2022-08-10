# created by Barry at 2022.06.22
from dataclasses import dataclass
from ..utils import read_description_from_odx

@dataclass()
class Ident_Value:
    type: str = None
    content: str = None


def read_ident_value(et_element):
    if et_element is None:
        return None
    type = et_element.get("TYPE")
    content = et_element.text
    return Ident_Value(type, content)


# OWN-IDENT are used for check purposes. for example, a test device needs the possibility to compare the current
# software version within the target device(ECU) with the new software version before reprogramming.
# A particular own-ident coud be a part number, a software version, or a supplier
@dataclass()
class Own_Ident:
    id: str = None
    short_name: str = None
    long_name: str = None
    description: str = None
    ident_value: Ident_Value = None


def read_own_ident(et_element):
    if et_element is None:
        return None
    id = et_element.get("ID")
    short_name = et_element.find("SHORT-NAME").text if et_element.find("SHORT-NAME") is not None else None
    long_name = et_element.find("LONG-NAME").text if et_element.find("LONG-NAME") is not None else None
    description = read_description_from_odx(et_element.find("DESC"))
    ident_value = read_ident_value(et_element.find("IDENT-VALUE"))
    return Own_Ident(id,
                     short_name,
                     long_name,
                     description,
                     ident_value)


