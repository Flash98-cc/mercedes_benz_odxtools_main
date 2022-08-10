# createde by Barry at 2022.06.22

from dataclasses import dataclass
from .own_ident import Own_Ident
from .session_desc import Diag_Comm_Snref, read_diag_comm_snref


@dataclass()
class Ident_If_Snref:
    short_name_snref: str = None
    ident_if: Own_Ident = None


def read_ident_if_snref(et_element):
    if et_element is None:
        return None
    short_name_snref = et_element.get("SHORT-NAME")
    return Ident_If_Snref(short_name_snref)


# TODO: Service::OUT-PARAM-IF how to define
@dataclass()
class Out_Param_If_Snref:
    pass


@dataclass()
class Ident_Desc:
    diag_comm_snref: Diag_Comm_Snref = None
    ident_if_snref: Ident_If_Snref = None


def read_ident_desc(et_element):
    if et_element is None:
        return None

    diag_comm_snref = read_diag_comm_snref(et_element.find("SHORT-NAME"))
    ident_if_snref = read_ident_if_snref(et_element.find("IDENT-IF-SNREF"))
    return Ident_Desc(diag_comm_snref, ident_if_snref)
