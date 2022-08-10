# SPDX-License-Identifier: MIT
# Copyright (c) 2022 MBition GmbH

from odxtools.audience import Audience, read_audience_from_odx
from odxtools.functionalclass import FunctionalClass
from odxtools.state import State
from odxtools.utils import read_description_from_odx
from odxtools.exceptions import DecodeError
from .odxtypes import DataType
from typing import List, Optional, Union
from enum import Enum

from .state_transition import StateTransition
from .structures import Request, Response
from .nameditemlist import NamedItemList
from .message import Message
from .parameters.valueparameter import ValueParameter
from .parameters.codedconstparameter import CodedConstParameter
from .parameters.physicalconstantparameter import PhysicalConstantParameter
from .parameters.tablekeyparameter import TableKeyParameter
from .odxtypes import DataType


class Trans_Mode(Enum):
    SEND_ONLY = "SEND-ONLY"
    RECEIVE_ONLY = "RECEIVE-ONLY"
    SEND_AND_RECEIVE = "SEND-AND-RECEIVE"
    SEND_OR_RECEIVE = "SEND-OR-RECEIVE"


# DIAG-SERVICE/POS-RESPONSE-SUPPRESSABLE: means the application can choose whether it expects a positive response or not
# ISO-22901-1 p65 figure 53
class Pos_Response_Suppressable:
    def __init__(self,
                 bit_mask: DataType.A_BYTEFIELD,
                 value_snref: str = None,
                 coded_const_snref: str = None,
                 phys_const_snref: str = None,
                 table_key_snref: str = None
                 ):
        self.table_key = None
        self.phys_const = None
        self.coded_const = None
        self.value = None
        self.bit_mask = bit_mask
        self.value_snref = value_snref
        self.coded_const_snref = coded_const_snref
        self.phys_const_snref = phys_const_snref
        self.table_key_snref = table_key_snref

        # self.value: ValueParameter
        # self.coded_const: CodedConstParameter
        # self.phys_const: PhysicalConstantParameter
        # self.table_key: TableKeyParameter
    # TODO: sn_lookup.params is not build, and services.resolve_snref_references function is not called by other function
    def resolve_snref_references(self, sn_lookup):
        if self.value_snref:
            self.value = sn_lookup.params[self.value_snref]
        if self.coded_const_snref:
            self.coded_const = sn_lookup.params[self.coded_const_snref]
        if self.phys_const_snref:
            self.phys_const = sn_lookup.params[self.phys_const_snref]
        if self.table_key_snref:
            self.table_key = sn_lookup.params[self.table_key_snref]


def read_pos_response_suppressable(et_element):
    if et_element is None:
        return None
    bit_mask = et_element.find("BIT-MASK")
    value_snref = et_element.find("VALUE-SNREF").get("SHORT-NAME") if et_element.find("VALUE-SNREF") is not None else None
    coded_const_snref = et_element.find("CODED-CONST-SNREF").get("SHORT-NAME") if et_element.find("CODED-CONST-SNREF") is not None else None
    phys_const_snref = et_element.find("PHYS-CODED-SNREF").get("SHORT-NAME") if et_element.find("PHYS-CODED-SNREF") is not None else None
    table_key_snref = et_element.find("TABLE-KEY-SNREF").get("SHORT-NAME") if et_element.find("TABLE-KEY-SNREF") is not None else None
    return Pos_Response_Suppressable(bit_mask,
                                     value_snref,
                                     coded_const_snref,
                                     phys_const_snref,
                                     table_key_snref
                                     )


class DiagService:
    def __init__(self,
                 id,
                 short_name,
                 request,
                 positive_responses: Union[List[str], List[Response]],
                 negative_responses: Union[List[str], List[Response]],
                 long_name=None,
                 description=None,
                 semantic=None,
                 audience: Optional[Audience] = None,
                 functional_class_refs=[],
                 pre_condition_state_refs=[],
                 state_transition_refs=[],
                 transmission_mode: Trans_Mode = Trans_Mode.SEND_AND_RECEIVE,
                 addressing: str = None,
                 pos_response_suppressable: Pos_Response_Suppressable = None
                 ):
        """Constructs the service.

        Parameters:
        ----------
        id: str
        short_name: str
            the short name of this DIAG-SERVICE
        request: str | Request
            the ID of a request or a object
        positive_responses: List[str] | List[Response]
        negative_responses: List[str] | List[Response]
        """
        self.id: str = id
        self.short_name: str = short_name
        self.long_name: Optional[str] = long_name
        self.description: Optional[str] = description
        self.semantic: Optional[str] = semantic
        self.audience: Optional[Audience] = audience
        self.transmission_mode = transmission_mode
        # used to define the addressing mode used by the diag-service
        self.addressing = addressing

        self.functional_class_refs: List[str] = functional_class_refs
        self._functional_classes: Union[List[FunctionalClass],
                                        NamedItemList[FunctionalClass]] = []
        self.pre_condition_state_refs: List[str] = pre_condition_state_refs
        self._pre_condition_states: Union[List[State],
                                          NamedItemList[State]] = []
        self.state_transition_refs: List[str] = state_transition_refs
        self._state_transitions: Union[List[StateTransition],
                                       NamedItemList[StateTransition]] = []

        self._request: Optional[Request]
        self.request_ref_id: str
        self._positive_responses: Optional[NamedItemList[Response]]
        self.pos_res_ref_ids: List[str]
        self._negative_responses: Optional[NamedItemList[Response]]
        self.neg_res_ref_ids: List[str]

        self.pos_response_suppressable = pos_response_suppressable

        if isinstance(request, str):
            self._request = None
            self.request_ref_id = request
        elif isinstance(request, Request):
            self._request = request
            self.request_ref_id = request.id
        elif request is None:
            self._request = None
            self.request_ref_id = None
        else:
            raise ValueError(
                "request must be a string (the ID of a request) or a Request object")

        if all(isinstance(x, Response) for x in positive_responses):
            # TODO (?): Can we tell mypy that positive_responses is definitely of type Iterable[Response]
            self._positive_responses = \
                NamedItemList[Response](lambda pr: pr.short_name,
                                        positive_responses)  # type: ignore
            self.pos_res_ref_ids = [
                pr.id for pr in positive_responses]  # type: ignore
        elif all(isinstance(x, str) for x in positive_responses):
            self._positive_responses = None
            self.pos_res_ref_ids = [str(r) for r in positive_responses]
        else:
            raise TypeError(
                "positive_responses must be of type Union[List[str], List[Response], None]")

        if all(isinstance(x, Response) for x in negative_responses):
            self._negative_responses = \
                NamedItemList[Response](lambda nr: nr.short_name,
                                        negative_responses)  # type: ignore
            self.neg_res_ref_ids = [
                nr.id for nr in negative_responses]  # type: ignore
        elif all(isinstance(x, str) for x in negative_responses):
            self._negative_responses = None
            self.neg_res_ref_ids = [str(r) for r in negative_responses]
        else:
            raise TypeError(
                "negative_responses must be of type Union[List[str], List[Response], None]")

    @property
    def request(self) -> Optional[Request]:
        return self._request

    @property
    def positive_responses(self) -> Optional[NamedItemList[Response]]:
        return self._positive_responses

    @property
    def negative_responses(self) -> Optional[NamedItemList[Response]]:
        return self._negative_responses

    @property
    def functional_classes(self):
        return self._functional_classes

    @property
    def pre_condition_states(self):
        return self._pre_condition_states

    @property
    def state_transitions(self):
        return self._state_transitions

    def _resolve_references(self, id_lookup):
        self._request = id_lookup.get(self.request_ref_id)
        self._positive_responses = \
            NamedItemList(
                lambda pr: pr.short_name,
                [id_lookup.get(pr_id) for pr_id in self.pos_res_ref_ids])
        self._negative_responses = \
            NamedItemList(
                lambda nr: nr.short_name,
                [id_lookup.get(nr_id) for nr_id in self.neg_res_ref_ids])
        self._functional_classes = \
            NamedItemList(
                lambda fc: fc.short_name,
                [id_lookup.get(fc_id) for fc_id in self.functional_class_refs])
        self._pre_condition_states = \
            NamedItemList(
                lambda st: st.short_name,
                [id_lookup.get(st_id) for st_id in self.pre_condition_state_refs])
        self._state_transitions = \
            NamedItemList(
                lambda st: st.short_name,
                [id_lookup.get(stt_id) for stt_id in self.state_transition_refs])
        if self.audience:
            self.audience._resolve_references(id_lookup)

    def resolve_snref_references(self, sn_lookup):
        if self.pos_response_suppressable:
            self.pos_response_suppressable.resolve_snref_references(sn_lookup)


    def decode_message(self, message: Union[bytes, bytearray]) -> Message:

        # Check if message is a request or positive or negative response
        interpretable_message_types = []

        if self.request is None or self.positive_responses is None or self.negative_responses is None:
            raise ValueError("References couldn't be resolved or have not been resolved yet."
                             " Try calling `database.resolve_references()`.")

        for message_type in [self.request,
                             *self.positive_responses,
                             *self.negative_responses]:
            prefix = message_type.coded_const_prefix(
                request_prefix=self.request.coded_const_prefix())
            if all(b == message[i] for (i, b) in enumerate(prefix)):
                interpretable_message_types.append(message_type)

        if len(interpretable_message_types) != 1:
            raise DecodeError(
                f"The service {self.short_name} cannot decode the message {message.hex()}")
        message_type = interpretable_message_types[0]
        param_dict = message_type.decode(message)
        return Message(coded_message=message, service=self, structure=message_type, param_dict=param_dict)

    def encode_request(self, **params):
        """
        Composes an UDS request as list of bytes for this service.
        Parameters:
        ----------
        params: dict
            Parameters of the RPC as mapping from SHORT-NAME of the parameter to the physical value
        """
        # make sure that all parameters which are required for
        # encoding are specified (parameters which have a default are
        # optional)
        missing_params = set(map(
            lambda x: x.short_name, self.request.get_required_parameters())).difference(params.keys())
        assert not missing_params, f"The parameters {missing_params} are required but missing!"

        # make sure that no unknown parameters are specified
        rq_all_param_names = set(
            map(lambda x: x.short_name, self.request.parameters))
        assert set(params.keys()).issubset(rq_all_param_names), \
            f"Unknown parameters specified for encoding: {params.keys()}, known parameters are: {rq_all_param_names}"
        return self.request.encode(**params)

    def encode_positive_response(self, coded_request, response_index=0, **params):
        # TODO: Should the user decide the positive response or what are the differences?
        return self.positive_responses[response_index].encode(coded_request, **params)

    def encode_negative_response(self, coded_request, response_index=0, **params):
        return self.negative_responses[response_index].encode(coded_request, **params)

    def __call__(self, **params) -> bytes:
        """Encode a request."""
        return self.encode_request(**params)

    def __str__(self):
        return f"DiagService(id={self.id}, semantic={self.semantic})"

    def __repr__(self):
        return self.__str__()

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, o: object) -> bool:
        return isinstance(o, DiagService) and self.id == o.id


def read_diag_service_from_odx(et_element):
    # logger.info(f"Parsing service based on ET DiagService element: {et_element}")
    short_name = et_element.find("SHORT-NAME").text
    id = et_element.get("ID")
    # ("SERVICE ID: ",id)

    request_ref_id = et_element.find("REQUEST-REF").get("ID-REF") if et_element.find("REQUEST-REF") is not None else None

    pos_res_ref_ids = [
        el.get("ID-REF") for el in et_element.iterfind("POS-RESPONSE-REFS/POS-RESPONSE-REF")
    ]
    neg_res_ref_ids = [
        el.get("ID-REF") for el in et_element.iterfind("NEG-RESPONSE-REFS/NEG-RESPONSE-REF")
    ]
    functional_class_ref_ids = [
        el.get("ID-REF") for el in et_element.iterfind("FUNCT-CLASS-REFS/FUNCT-CLASS-REF")
    ]
    pre_condition_state_ref_ids = [
        el.get("ID-REF") for el in et_element.iterfind("PRE-CONDITION-STATE-REFS/PRE-CONDITION-STATE-REF")
    ]
    state_transition_ref_ids = [
        el.get("ID-REF") for el in et_element.iterfind("STATE-TRANSITION-REFS/STATE-TRANSITION-REF")
    ]
    long_name = et_element.find(
        "LONG-NAME").text if et_element.find("LONG-NAME") is not None else None

    description = read_description_from_odx(et_element.find("DESC"))
    semantic = et_element.get("SEMANTIC")

    audience = read_audience_from_odx(et_element.find(
        "AUDIENCE")) if et_element.find("AUDIENCE") else None

    addressing = et_element.get("ADDRESSING") if et_element.get("ADDRESSING") is not None else None

    transmission_mode = et_element.get("TRANSMISSION-MODE") if et_element.get("TRANSMISSION-MODE") is not None else None
    for trans_mode in Trans_Mode:
        if trans_mode.value == transmission_mode:
            transmission_mode = trans_mode

    pos_response_suppressable = read_pos_response_suppressable(et_element.find("POS-RESPONSE-SUPPRESSABLE"))

    diag_service = DiagService(id,
                               short_name,
                               request_ref_id,
                               pos_res_ref_ids,
                               neg_res_ref_ids,
                               long_name=long_name,
                               description=description,
                               semantic=semantic,
                               audience=audience,
                               functional_class_refs=functional_class_ref_ids,
                               pre_condition_state_refs=pre_condition_state_ref_ids,
                               state_transition_refs=state_transition_ref_ids,
                               transmission_mode=transmission_mode,
                               addressing=addressing,
                               pos_response_suppressable=pos_response_suppressable)
    return diag_service
