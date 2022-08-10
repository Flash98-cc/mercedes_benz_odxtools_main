# created by Barry at 2022.6.15
from typing import Optional

from ..admindata import AdminData
from ..companydata import CompanyData
from ..admindata import read_admin_data_from_odx
from ..companydata import read_company_datas_from_odx
from ..utils import read_description_from_odx
from .info_component import Info_Component, read_info_component_from_odx
from .vehicle_information import Vehicle_Information, read_vehicle_information_from_odx


class Vehicle_Info_Spec:
    def __init__(self,
                 id,
                 short_name,
                 long_name,
                 admin_data: Optional[AdminData] = None,
                 company_data: Optional[CompanyData] = None,
                 description: str = None,
                 info_components: list[Info_Component] = None,
                 vehicle_informations: list[Vehicle_Information] = None
                 ):
        self.id = id
        self.short_name = short_name
        self.long_name = long_name
        self.admin_data = admin_data
        self.company_data = company_data
        self.description = description
        self.info_components = info_components
        self.vehicle_informations = vehicle_informations

    def _build_id_lookup(self, id_lookup):
        pass

    def _resolve_references(self, id_lookup):
        pass


def read_vehicle_info_spec_from_odx(et_element, enable_candela_workarounds=True):
    id = et_element.get("ID")
    short_name = et_element.find("SHORT-NAME").text if et_element.find("SHORT-NAME") is not None else None
    long_name = et_element.find("LONG-NAME").text if et_element.find("LONG-NAME") is not None else None
    admin_data = read_admin_data_from_odx(et_element.find("ADMIN-DATA")) \
        if et_element.find("ADMIN-DATA") is not None else None

    company_datas = read_company_datas_from_odx(et_element.find("COMPANY-DATA")) \
        if et_element.find("COMPANY-DATA") is not None else None

    description = read_description_from_odx(et_element.find("DESC")) if et_element.find("DESC") is not None else None

    info_components = [read_info_component_from_odx(el)
                       for el in et_element.iterfind("INFO-COMPONENTS/INFO-COMPONENT")] \
        if et_element.find("INFO-COMPONENTS/INFO-COMPONENT") is not None else None

    vehicle_informations = [read_vehicle_information_from_odx(el)
                            for el in et_element.iterfind("VEHICLE-INFORMATIONS/VEHICLE-INFORMATION")] \
        if et_element.find("VEHICLE-INFORMATIONS/VEHICLE-INFORMATION") is not None else None

    return Vehicle_Info_Spec(id,
                             short_name,
                             long_name,
                             admin_data,
                             company_datas,
                             description,
                             info_components,
                             vehicle_informations
                             )
