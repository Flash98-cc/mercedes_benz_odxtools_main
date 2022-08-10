# created by Barry at 2022.06.22
from dataclasses import dataclass

from ..diaglayer import read_short_name, read_long_name
from ..utils import read_description_from_odx


# used to group sessions according to certain criteria.
@dataclass()
class Flash_Class:
    id: str = None
    short_name: str = None
    long_name: str = None
    description: str = None


def read_flash_class(et_element):
    if et_element is None:
        return None
    id = et_element.get("ID")
    short_name = read_short_name(et_element.find("SHORT-NAME"))
    long_name = read_long_name(et_element.find("LONG-NANE"))
    description = read_description_from_odx(et_element.find("DESC"))
    return Flash_Class(id,
                       short_name,
                       long_name,
                       description)
