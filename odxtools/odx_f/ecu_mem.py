# p236 figure 152
# created by Barry at 2022.06.21
from dataclasses import dataclass
from typing import Optional

from ..admindata import AdminData, read_admin_data_from_odx
from ..companydata import CompanyData, read_company_datas_from_odx
from .mem import Mem, read_mem_from_odx
from .phys_mem import Phys_Mem, read_phys_mem_from_odx
from ..utils import read_description_from_odx


@dataclass()
class Ecu_Mem:
    id: str = None
    oid: str = None
    short_name: str = None
    long_name: str = None
    description: str = None
    admin_data: Optional[AdminData] = None
    mem: Optional[Mem] = None
    phys_mem: Optional[Phys_Mem] = None

    def _build_id_lookup(self, id_lookup):
        pass

    def _resolve_references(self, id_lookup):
        pass


def read_ecu_mem_from_odx(et_element):
    if et_element is None:
        return None

    id = et_element.get("ID")
    oid = et_element.get("OID") if et_element.get("OID") is not None else None
    short_name = et_element.find("SHORT-NAME").text if et_element.find("SHORT-NAME") is not None else None
    long_name = et_element.find("LONG-NAME").text if et_element.find("LONG-NAME") is not None else None
    description = read_description_from_odx(et_element.find("DESC"))
    admin_data = read_admin_data_from_odx(et_element.find("ADMIN-DATA"))
    mem = read_mem_from_odx(et_element.find("MEM"))
    phys_mem = read_phys_mem_from_odx(et_element.find("PHYS-MEM"))

    return Ecu_Mem(id,
                   oid,
                   short_name,
                   long_name,
                   description,
                   admin_data,
                   mem,
                   phys_mem)






