# created by Barry at 2022/5/31 

from itertools import chain
from typing import Optional, Any, Dict, Iterable, List, Union

from ..exceptions import *
from ..globals import logger, xsi
from ..state import read_state_from_odx
from ..state_transition import read_state_transition_from_odx

from ..utils import read_description_from_odx
from ..nameditemlist import NamedItemList
from ..admindata import AdminData, read_admin_data_from_odx
from ..companydata import CompanyData, read_company_datas_from_odx
# from ..communicationparameter import CommunicationParameterRef, read_communication_param_ref_from_odx
from ..diagdatadictionaryspec import DiagDataDictionarySpec, read_diag_data_dictionary_spec_from_odx
from ..dataobjectproperty import DopBase
from ..functionalclass import read_functional_class_from_odx
from ..audience import read_additional_audience_from_odx
from ..message import Message
from ..service import DiagService, read_diag_service_from_odx
from ..singleecujob import SingleEcuJob, read_single_ecu_job_from_odx
from ..structures import Request, Response, read_structure_from_odx
from .protstack import *
from dataclasses import dataclass
from ..parent_dl import Parent_Dl


class Comparam_Spec:
    def __init__(self,
                 id,
                 short_name,
                 long_name=None,
                 description=None,
                 admin_data: Optional[AdminData] = None,
                 company_datas: Optional[NamedItemList[CompanyData]] = None,
                 prot_stacks=[]):
        self.id = id
        self.short_name = short_name
        self.long_name = long_name
        self.description = description
        self.admin_data = admin_data
        self.company_datas = company_datas
        self.prot_stacks = prot_stacks

    def _build_sn_lookup(self, sn_lookup: Parent_Dl()):
        pass

    def _resolve_references(self, id_lookup):
        pass


@dataclass()
class Comparam_Spec_Ref:
    id_ref: str = None
    comparam_spec: Comparam_Spec = None


def read_comparam_spec_ref(et_element):
    if et_element is None:
        return None
    id_ref = et_element.get("ID-REF")
    return Comparam_Spec_Ref(id_ref)


def read_comparam_spec_from_odx(et_element, enable_candela_workarounds=True):
    id = et_element.get("ID")  # get()用于获取属性
    short_name = et_element.find("SHORT-NAME").text  # find是找到子元素
    long_name = et_element.find("SHORT-NAME").text if et_element.find("SHORT-NAME") is not None else None

    description = read_description_from_odx(et_element.find("DESC"))
    if description is not None:
        description = description
    else:
        description = None

    if et_element.find("ADMIN-DATA"):
        admin_data = read_admin_data_from_odx(et_element.find("ADMIN-DATA"))
    else:
        admin_data = None

    if et_element.find("COMPANY-DATAS"):
        company_datas = read_company_datas_from_odx(et_element.find("COMPANY-DATAS"))
    else:
        company_datas = None

    prot_stacks = [read_prot_stack_from_odx(dl_element, enable_candela_workarounds=enable_candela_workarounds)
                   for dl_element in et_element.iterfind("PROT-STACKS/PROT-STACK")]

    return Comparam_Spec(id=id,
                         short_name=short_name,
                         long_name=long_name,
                         description=description,
                         admin_data=admin_data,
                         company_datas=company_datas,
                         prot_stacks=prot_stacks
                         )
