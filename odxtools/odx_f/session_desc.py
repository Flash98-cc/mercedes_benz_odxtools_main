# created by Barry at 2022.06.22
# see figure 158 for more details
from dataclasses import dataclass
from enum import Enum
from ..diaglayer import read_short_name, read_long_name
from ..utils import read_description_from_odx
from ..audience import Audience, read_audience_from_odx
from .session import Session
from .flash_class import Flash_Class
from .own_ident import Own_Ident, read_own_ident


class DIRECTION(Enum):
    DOWNLOAD = "DOWNLOAD"
    UPLOAD = "UPLOAD"


@dataclass()
class Session_Snref:
    short_name_snref: str = None
    session: Session = None


def read_session_snref(et_element):
    if et_element is None:
        return None
    short_name_snref = et_element.get("SHORT-NAME")
    return Session_Snref(short_name_snref)


# Diag_Comm_Snref is an optional element
@dataclass()
class Diag_Comm_Snref:
    short_name_snref: str = None
    # TODO: diag-comm structure


def read_diag_comm_snref(et_element):
    if et_element is None:
        return None
    short_name_snref = et_element.get("SHORT-NAME")
    return Diag_Comm_Snref(short_name_snref)


@dataclass()
class Flash_Class_Ref:
    id_ref: str = None
    flash_class: Flash_Class = None


def read_flash_class_ref(et_element):
    if et_element is None:
        return None
    id_ref = et_element.find("ID-REF")
    return Flash_Class_Ref(id_ref)


# used to store information about sessions and jobs used for download or upload
@dataclass()
class Session_Desc:
    oid: str = None
    # short_name of session_descs in all ecu_mem_connectors should be unique
    short_name: str = None
    long_name: str = None
    description: str = None
    # specifieds whether it is a download or upload session
    direction: DIRECTION = None
    partnumber: str = None
    # defines the priority of the session, higher session will execute first, range from [0,100], 0 is highest priority
    priority: int = 100
    audience: Audience = None
    own_ident: Own_Ident = None
    flash_class_refs: list[Flash_Class_Ref] = None

    diag_comm_snref: Diag_Comm_Snref = None
    session_snref: Session_Snref = None

    def _resolve_references(self, id_lookup):
        if self.flash_class_refs is not None:
            for flash_class_ref in self.flash_class_refs:
                flash_class_ref.flash_class = id_lookup[flash_class_ref.id_ref]

        # TODO: how to resolve diag_comm_snref and session_snref references


def read_session_desc(et_element):
    if et_element is None:
        return None
    oid = et_element.get("OID") if et_element.get("OID") is not None else None
    direction = et_element.get("DIRECTION") if et_element.get("DIRECTION") is not None else None
    short_name = read_short_name(et_element.find("SHORT-NAME"))
    long_name = read_long_name(et_element.find("LONG-NAME"))
    description = read_description_from_odx(et_element.find("DESC"))
    partnumber = et_element.find("PARTNUMBER").text
    priority = et_element.find("PRIORITY").text
    priority = int(priority)
    audience = read_audience_from_odx(et_element.find("AUDIENCE"))
    own_ident = read_own_ident(et_element.find("OWN-IDENT"))
    flash_class_refs = [read_flash_class_ref(el)
                        for el in et_element.iterfind("FLASH-CALSSS/FLASH-CLASS")]
    diag_comm_snref = read_diag_comm_snref(et_element.find("DIAG-COMM-SNREF"))
    session_snref = read_session_snref(et_element.find("SESSION-SNREF"))

    return Session_Desc(oid,
                        short_name,
                        long_name,
                        description,
                        direction,
                        partnumber,
                        priority,
                        audience,
                        own_ident,
                        flash_class_refs,
                        diag_comm_snref,
                        session_snref)

