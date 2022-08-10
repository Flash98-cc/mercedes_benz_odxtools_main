# p236 figure 152
# created by Barry at 2022.06.21
from dataclasses import dataclass
from typing import Optional

from .session import Session, read_session_from_mem
from .datablock import Datablock, read_datablock_from_mem
from .flashdata import Flashdata, read_flashdata_from_mem

from ..nameditemlist import NamedItemList


@dataclass()
class Mem:
    sessions: list[Session] = None
    datablocks: list[Datablock] = None
    flashdatas: list[Flashdata] = None

    def _build_id_lookup(self, id_lookup):
        if self.datablocks is not None:
            for datablock in self.datablocks:
                id_lookup[datablock.id] = datablock

        if self.flashdatas is not None:
            for flashdata in self.flashdatas:
                id_lookup[flashdata.id] = flashdata

    def _resolve_references(self, id_lookup):
        if self.sessions is not None:
            for session in self.sessions:
                session._resolve_references(id_lookup)
        if self.datablocks is not None:
            for datablock in self.datablocks:
                datablock._resolve_references(id_lookup)


def read_mem_from_odx(et_element):
    sessions = [read_session_from_mem(el)
                for el in et_element.iterfind("SESSIONS/SESSION")]
    # sessions = None

    datablocks = [read_datablock_from_mem(el)
                  for el in et_element.iterfind("DATABLOCKS/DATABLOCK")]

    flashdatas = [read_flashdata_from_mem(el)
                  for el in et_element.iterfind("FLASHDATAS/FLASHDATA")]

    return Mem(sessions,
               datablocks,
               flashdatas)
