from ctypes.wintypes import BOOLEAN
from enum import Enum
from typing import Optional, Dict, Any
from dataclasses import dataclass

from ..units import UnitSpec, read_unit_spec_from_odx
from ..utils import read_description_from_odx
from ..dataobjectproperty import DataObjectProperty, read_data_object_property_from_odx
from ..parent_dl import Parent_Dl

# TODO admindata and companydata are not parsed


class USAGE(Enum):
    ECU_SOFTWARE = "ECU-SOFTWARE"
    ECU_COMM = "ECU-COMM"
    APPLICATION = "APPLICATION"
    TESTER = "TESTER"


class Comparam:
    def __init__(self,
                 id: str,
                 display_level: int,
                 param_class: str = None,
                 cptype: str = None,
                 cpusage: Optional[USAGE] = None,
                 short_name: Optional[str] = None,
                 long_name: str = None,
                 description: str = None,
                 physical_default_value: str = None,
                 data_object_prop_ref=None):
        self.id = id
        self.param_class = param_class
        self.cptype = cptype

        self.cpuusage = cpusage

        self.display_level = display_level
        self.short_name = short_name
        self.long_name = long_name
        self.description = description
        self.physical_default_value = physical_default_value
        self.data_object_prop_ref = data_object_prop_ref

    def _resolve_references(self, id_lookup):
        pass


def read_comparam_from_odx(et_element):
    id = et_element.get("ID")
    param_class = et_element.get("PARAM-CLASS") if et_element.get("PARAM-CLASS") is not None else None
    cptype = et_element.get("CPTYPE") if et_element.get("CPTYPE") is not None else None
    cpusage = None
    # parse USAGE
    for usage in USAGE:
        if usage.value == et_element.get("CPUSAGE"):
            cpusage = usage
    short_name = et_element.find("SHORT-NAME").text if et_element.find("SHORT-NAME") is not None else None
    long_name = et_element.find("LONG-NAME").text if et_element.find("LONG-NAME") is not None else None
    description = read_description_from_odx(et_element.find("DESC")) if et_element.find("DESC") is not None else None

    physical_default_value = et_element.find("PHYSICAL-DEFAULT-VALUE").text \
        if et_element.find("PHYSICAL-DEFAULT-VALUE") is not None else None

    data_object_prop_ref = et_element.find("DATA-OBJECT-PROP-REF").get("ID-REF") \
        if et_element.find("DATA-OBJECT-PROP-REF") is not None else None

    display_level = et_element.get("DISPLAY-LEVEL") if et_element.get("DISPLAY-LEVEL") is not None else None

    return Comparam(
        id=id,
        display_level=display_level,
        param_class=param_class,
        cptype=cptype,
        cpusage=cpusage,
        short_name=short_name,
        long_name=long_name,
        description=description,
        physical_default_value=physical_default_value,
        data_object_prop_ref=data_object_prop_ref)


class Complex_Comparam:
    def __init__(self,
                 id: str,
                 display_level: int,
                 allow_multiple_values: bool = True,
                 complex_physical_default_value: str = None,
                 short_name: str = None,
                 long_name: str = None,
                 description: str = None,
                 param_class: str = None,
                 cptype: str = None,
                 cpusage: [USAGE] = None,
                 comparams: list[Comparam] = None
                 ):
        self.id = id
        self.display_level = display_level
        self.allow_multiple_values = allow_multiple_values
        self.complex_physical_default_value = complex_physical_default_value
        self.short_name = short_name
        self.long_name = long_name
        self.description = description
        self.param_class = param_class
        self.cptype = cptype

        for usage in USAGE:
            if usage == cpusage:
                self.cpusage = cpusage
        self.comparams = comparams

    def resolve_references(self, id_lookup:Dict[str, Any]):
        pass


def read_complex_comparam_from_odx(et_element):
    id = et_element.get("ID")
    param_class = et_element.get("PARAM-CLASS") if et_element.get("PARAM-CLASS") is not None else None
    cptype = et_element.get("CPTYPE") if et_element.get("CPTYPE") is not None else None
    cpusage = et_element.get("CPUSAGE") if et_element.get("CPUSAGE") is not None else None

    if et_element.get("ALLOW_MULTIPLE_VALUES") == "true":
        allow_multiple_values = True
    elif et_element.get("ALLOW_MULTIPLE_VALUES") == "false":
        allow_multiple_values = False
    else:
        allow_multiple_values = None

    display_level = et_element.get("DISPLAY-LEVEL") if et_element.get("DISPLAY-LEVEL") is not None else None

    short_name = et_element.find("SHORT-NAME").text if et_element.find("SHORT-NAME") is not None else None
    long_name = et_element.find("LONG-NAME").text if et_element.find("LONG-NAME") is not None else None
    description = read_description_from_odx(et_element.find("DESC")) if et_element.find("DESC") is not None else None

    complex_physical_default_value = et_element.find("COMPLEX-PHYSICAL-DEFAULT-VALUE").text \
        if et_element.find("COMPLEX-PHYSICAL-DEFAULT-VALUE") is not None else None

    comparams = [read_comparam_from_odx(el)
                 for el in et_element.iterfind("COMPARAM")]
    return Complex_Comparam(id=id,
                            display_level=display_level,
                            allow_multiple_values=allow_multiple_values,
                            complex_physical_default_value=complex_physical_default_value,
                            short_name=short_name,
                            long_name=long_name,
                            description=description,
                            param_class=param_class,
                            cptype=cptype,
                            cpusage=cpusage,
                            comparams=comparams
                            )


class ComparamSubset:
    def __init__(self,
                 id: str,
                 category: str,
                 short_name=None,
                 long_name=None,
                 description=None,
                 comparams: list[Comparam] = None,
                 complex_comparams: list[Complex_Comparam] = None,
                 data_object_props: list[DataObjectProperty] = None,
                 unit_spec: Optional[UnitSpec] = None
                 ):
        self.id = id
        self.category = category
        self.short_name = short_name
        self.long_name = long_name
        self.description = description
        self.comparams = comparams
        self.complex_comparams = complex_comparams
        self.data_object_props = data_object_props
        self.unit_spec = unit_spec

    def _build_id_lookup(self, id_lookup: Dict[str, Any]):
        pass


def read_comparam_subset_from_odx(et_element, enable_candela_workarounds=True):
    id = et_element.get("ID")
    category = et_element.get("CATEGORY") if et_element.get("CATEGORY") is not None else None
    short_name = et_element.find("SHORT-NAME").text if et_element.find("SHORT-NAME") is not None else None
    long_name = et_element.find("LONG-NAME").text if et_element.find("LONG-NAME") is not None else None
    description = read_description_from_odx(et_element.find("DESC")) if et_element.find("DESC") is not None else None

    comparams = [read_comparam_from_odx(el)
                 for el in et_element.iterfind("COMPARAMS/COMPARAM")]

    complex_comparams = [read_complex_comparam_from_odx(el)
                         for el in et_element.iterfind("COMPLEX-COMPARAMS/COMPLEX-COMPARAM")]

    data_object_props = [read_data_object_property_from_odx(el)
                         for el in et_element.iterfind("DATA-OBJECT-PROPS/DATA-OBJECT-PROP")]

    unit_spec = read_unit_spec_from_odx(et_element.find("UNIT-SPEC"))

    return ComparamSubset(id=id,
                          category=category,
                          short_name=short_name,
                          long_name=long_name,
                          description=description,
                          comparams=comparams,
                          complex_comparams=complex_comparams,
                          data_object_props=data_object_props,
                          unit_spec=unit_spec)


@dataclass()
class Comparam_Ref:
    id_ref: str = None
    comparam: Comparam = None


def read_comparam_ref(et_element):
    if et_element is None:
        return None
    id_ref = et_element.get("ID-REF")
    return Comparam_Ref(id_ref)
