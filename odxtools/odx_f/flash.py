# created by Barry at 2022.06.21
# flash file is the entrance for odx-f file
# please see 7.5 ODX data model for ECU memory programming
from dataclasses import dataclass
from typing import Optional

from ..admindata import AdminData, read_admin_data_from_odx
from ..companydata import CompanyData, read_company_datas_from_odx
from ..nameditemlist import NamedItemList
from ..utils import read_description_from_odx
from ..audience import AdditionalAudience, read_additional_audience_from_odx
from .ecu_mem import Ecu_Mem, read_ecu_mem_from_odx
from .ecu_mem_connector import Ecu_Mem_Connector, read_ecu_mem_connector_from_odx


@dataclass()
class Flash:
    id: str = None
    short_name: str = None
    long_name: str = None
    desc: str = None
    admin_data: Optional[AdminData] = None
    company_datas: list[CompanyData] = None
    additional_audience: Optional[AdditionalAudience] = None
    ecu_mems: list[Ecu_Mem] = None
    ecu_mem_connectors: list[Ecu_Mem_Connector] = None

    # def _build_id_lookup(self, id_lookup):
    #     if self.ecu_mems is not None:
    #         for ecu_mem in self.ecu_mems:
    #             id_lookup[ecu_mem.id] = ecu_mem
    #
    #     if self.ecu_mem_connectors is not None:
    #         for ecu_mem_connector in self.ecu_mem_connectors:
    #             ecu_mem_connector._build_id_lookup(id_lookup)
    #
    # def _resolve_references(self, id_lookup):
    #     if self.ecu_mems is not None:
    #         for ecu_mem in self.ecu_mems:
    #             ecu_mem._resolve_references(id_lookup)
    #
    #     if self.ecu_mem_connectors is not None:
    #         for ecu_mem_connector in self.ecu_mem_connectors:
    #             ecu_mem_connector._resolve_references(id_lookup)


def read_flash_from_odx(et_element, enable_candela_workarounds=True):
    id = et_element.get("ID")
    short_name = et_element.find("SHORT-NAME").text if et_element.find("SHORT-NAME") is not None else None
    long_name = et_element.find("LONG-NAME").text if et_element.find("LONG-NAME") is not None else None
    desc = read_description_from_odx(et_element.find("DESC")) if et_element.find("DESC") is not None else None
    admin_data = read_admin_data_from_odx(et_element.find("ADMIN-DATA"))
    company_datas = read_company_datas_from_odx(et_element.find("COMPANY-DATAS"))
    additional_audience = read_additional_audience_from_odx(et_element.find("ADDITIONAL-AUDIENCE"))

    ecu_mems = [read_ecu_mem_from_odx(el)
                for el in et_element.iterfind("ECU-MEMS/ECU-MEM")]

    ecu_mem_connectors = [read_ecu_mem_connector_from_odx(el)
                          for el in et_element.iterfind("ECU-MEM-CONNECTORS/ECU-MEM-CONNECTOR")]

    return Flash(id,
                 short_name,
                 long_name,
                 desc,
                 admin_data,
                 company_datas,
                 additional_audience,
                 ecu_mems,
                 ecu_mem_connectors)
