# SPDX-License-Identifier: MIT
# Copyright (c) 2022 MBition GmbH
from typing import Dict, Any
from dataclasses import dataclass

from odxtools.utils import read_description_from_odx
from .odx_c.protstack import Prot_Stack_Snref, read_prot_stack_snref
from .protocol import Protocol_Snref, read_protocol_snref
from .odx_cs.comparamsubset import Comparam_Ref, read_comparam_ref
from .parent_dl import Parent_Dl


@dataclass()
class CommunicationParameterRef:
    value: str
    description: str
    id_ref: str = None
    comparam_ref: Comparam_Ref = None
    prot_stack_snref: Prot_Stack_Snref = None
    protocol_snref: Protocol_Snref = None

    # def __init__(self,
    #              value,
    #              id_ref,
    #              description=None,
    #              protocol_sn_ref=None,
    #              prot_stack_sn_ref=None):
    #     self.comparam_ref: Comparam_Ref = None
    #     self.comparam_ref.id_ref = id_ref
    #     self.prot_stack_snref: Prot_Stack_Snref = None
    #     self.prot_stack_snref.snref = prot_stack_sn_ref
    #     self.protocol_snref: Diaglayer_Snref = None
    #     self.protocol_snref.snref = protocol_sn_ref
    #
    #     self.value = value
    #     self.id_ref = id_ref
    #
    #     self.description = description
    #     self.protocol_sn_ref = protocol_sn_ref
    #     self.prot_stack_sn_ref = prot_stack_sn_ref

    def resolve_references(self, id_lookup: Dict[str, Any]):
        if self.comparam_ref is not None and self.comparam_ref.id_ref in id_lookup.keys():
            self.comparam_ref.comparam = id_lookup[self.comparam_ref.id_ref]

    def resolve_snref_references(self, sn_lookup: Parent_Dl()):
        pass

    def __repr__(self) -> str:
        val = self.value
        if not isinstance(self.value, list):
            val = f"'{val}'"

        return f"CommunicationParameter('{self.id_ref}', value={val})"

    def __str__(self) -> str:
        val = self.value
        if not isinstance(self.value, list):
            val = f"'{val}'"

        return f"CommunicationParameter('{self.id_ref}', value={val})"

    def _python_name(self):
        return self.id_ref.replace(".", "__")


def _read_complex_value_from_odx(et_element):
    result = []
    for el in et_element.findall("*"):
        if el.tag == "SIMPLE-VALUE":
            result.append('' if el.text is None else el.text)
        else:
            result.append(_read_complex_value_from_odx(el))
    return result


def read_communication_param_ref_from_odx(et_element):
    id_ref = et_element.get("ID-REF")

    if et_element.find("SIMPLE-VALUE") is not None:
        value = et_element.find("SIMPLE-VALUE").text
    else:
        value = _read_complex_value_from_odx(et_element.find("COMPLEX-VALUE"))

    description = read_description_from_odx(et_element.find("DESC"))

    comparam_ref = read_comparam_ref(et_element)

    protocol_snref = read_protocol_snref(et_element.find("PROTOCOL-SNREF"))

    prot_stack_snref = read_prot_stack_snref(et_element.find("PROT-STACK-SNREF"))

    return CommunicationParameterRef(value,
                                     description,
                                     id_ref,
                                     comparam_ref,
                                     prot_stack_snref,
                                     protocol_snref
                                     )
