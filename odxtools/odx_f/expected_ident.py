# created by Barry at 2022.06.22
from dataclasses import dataclass
from enum import  Enum

from ..odxtypes import DataType
from ..utils import read_description_from_odx


@dataclass()
class Ident_Value:
    type: DataType = None
    content: str = None


def read_ident_value_from_expected_ident(et_element):
    if et_element is None:
        return None
    type = et_element.get("TYPE")
    content = et_element.text
    return Ident_Value(type,
                       content)


@dataclass()
class Expected_Ident:
    id: str = None
    oid: str = None
    short_name: str = None
    long_name: str = None
    description: str = None
    ident_values: list[Ident_Value] = None


def read_expeced_ident(et_element):
    if et_element is None:
        return None

    id = et_element.get("ID")
    oid = et_element.get("OID") if et_element.get("OID") is not None else None
    short_name = et_element.find("SHORT-NAME").text if et_element.find("SHORT-NAME") is not None else None
    long_name = et_element.find("LONG-NAME").text if et_element.find("LONG-NAME") is not None else None
    description = read_description_from_odx(et_element.find("DESC"))
    ident_values = [read_ident_value_from_expected_ident(el)
                    for el in et_element.iterfind("IDENT-VALUES/IDENT-VALUE")]

    return Expected_Ident(id,
                          oid,
                          short_name,
                          long_name,
                          description,
                          ident_values
                          )









