# p237 figure 153
# created by Barry at 2022.06.21
# see 7.5.2.2 for more details
from dataclasses import dataclass

from .datablock import Datablock
from ..utils import read_description_from_odx
from .expected_ident import Expected_Ident, read_expeced_ident
from .checksum import CheckSum, read_checksum_from_odx
from .security import Security, read_security_from_session


@dataclass()
class DataBlock_Ref:
    id_ref: str = None
    DataBlock: Datablock = None


def read_datablock_ref_from_session(et_element):
    if et_element is None:
        return None
    id_ref = et_element.get("ID-REF")
    return DataBlock_Ref(id_ref)


# sessions are the only logical units that can be chosen for programming
@dataclass()
class Session:
    id: str = None
    oid: str = None
    short_name: str = None
    long_name: str = None
    description: str = None
    datablock_refs: list[DataBlock_Ref] = None
    expected_idents: list[Expected_Ident] = None
    # checksum is not defined
    checksums: list[CheckSum] = None
    securitys: list[Security] = None

    def _resolve_references(self, id_lookup):
        if self.datablock_refs is not None:
            for datablock_ref in self.datablock_refs:
                datablock_ref.DataBlock = id_lookup[datablock_ref.id_ref]


def read_session_from_mem(et_element):
    if et_element is None:
        return None

    id = et_element.get("ID")
    oid = et_element.get("OID")
    short_name = et_element.find("SHORT-NAME").text if et_element.find("SHORT-NAME") is not None else None
    long_name = et_element.find("LONG-NAME").text if et_element.find("LONG-NAME") is not None else None
    description = read_description_from_odx(et_element.find("DESC"))

    datablock_refs = [read_datablock_ref_from_session(el)
                      for el in et_element.iterfind("DATABLOCK-REFS/DATABLOCK-REF")]

    expected_idents = [read_expeced_ident(el)
                       for el in et_element.iterfind("EXPECTED-IDENTS/EXPECTED-IDENT")]

    # checksum is not defined
    checksums = [read_checksum_from_odx(el)
                 for el in et_element.iterfind("CHECKSUMS/CHECKSUM")]

    security = []
    if et_element.find("SECURITYS"):
        security = [read_security_from_session(el)
                    for el in et_element.iterfind("SECURITYS/SECURITY")]
    return Session(id,
                   oid,
                   short_name,
                   long_name,
                   description,
                   datablock_refs,
                   expected_idents,
                   checksums=checksums,
                   securitys=security)
