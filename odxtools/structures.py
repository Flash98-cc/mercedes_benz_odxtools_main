# SPDX-License-Identifier: MIT
# Copyright (c) 2022 MBition GmbH

from typing import Dict, Iterable, Optional, OrderedDict, Union

from .dataobjectproperty import DataObjectProperty, DopBase
from .decodestate import DecodeState, ParameterValuePair
from .encodestate import EncodeState
from .exceptions import DecodeError, EncodeError
from .globals import logger
from .nameditemlist import NamedItemList
from .parameters import Parameter, ParameterWithDOP, read_parameter_from_odx
from .parameters import CodedConstParameter, MatchingRequestParameter, ValueParameter
from .utils import read_description_from_odx


class BasicStructure(DopBase):
    def __init__(self,
                 id,
                 short_name,
                 parameters: Iterable[Parameter],
                 long_name=None,
                 byte_size=None,
                 description=None):
        super().__init__(id, short_name, long_name=long_name, description=description)
        self.parameters = NamedItemList(lambda par: par.short_name, parameters)

        self._byte_size = byte_size

    @property
    def bit_length(self):
        if self._byte_size:
            return 8 * self._byte_size
        elif all(p.bit_length is not None for p in self.parameters):
            return sum([p.bit_length for p in self.parameters])
        else:
            return None

    def coded_const_prefix(self, request_prefix: Union[bytes, bytearray] = bytes()):
        prefix = bytearray()
        encode_state = EncodeState(
            prefix, parameter_values={}, triggering_request=request_prefix)
        for p in self.parameters:
            if isinstance(p, CodedConstParameter) and p.bit_length % 8 == 0:
                prefix = p.encode_into_pdu(encode_state)
                encode_state = EncodeState(prefix, *encode_state[1:])
            elif isinstance(p, MatchingRequestParameter):
                prefix = p.encode_into_pdu(encode_state)
                encode_state = EncodeState(prefix, *encode_state[1:])
            else:
                break
        return prefix

    def get_required_parameters(self):
        return filter(lambda p: p.is_required(), self.parameters)

    def convert_physical_to_internal(self,
                                     param_values: dict,
                                     triggering_coded_request,
                                     is_end_of_pdu=True):
        logger.debug(f"{self.short_name} encode RPC"
                     f" with params={param_values}")

        coded_rpc = bytearray()
        encode_state = EncodeState(coded_rpc,
                                   param_values,
                                   triggering_request=triggering_coded_request,
                                   is_end_of_pdu=False)

        # Keep track of the expected length. (This is just to double check and not actually needed.)
        bit_length: Optional[int] = 0
        for param in self.parameters:
            if param == self.parameters[-1]:
                # The last parameter is at the end of the PDU iff the structure itself is at the end of the PDU
                encode_state = encode_state._replace(
                    is_end_of_pdu=is_end_of_pdu)
                if isinstance(param, ValueParameter) and hasattr(param.dop, 'min_number_of_items'):
                    # The param repeats itself, making bit_length calculation invalid
                    # Temporary workaround
                    # Can not import EndOfPduField to check on its type due to circular dependency
                    bit_length = None
            coded_rpc = param.encode_into_pdu(encode_state)
            encode_state = encode_state._replace(coded_message=coded_rpc)

            # Compute expected length
            if bit_length is not None and param.bit_length is not None:
                bit_length = bit_length + param.bit_length
            else:
                bit_length = None

        # Assert that length is as expected
        if bit_length is not None:
            assert bit_length % 8 == 0, f"Length of coded structure is not divisible by 8, i.e. is not a full sequence of bytes."
            assert len(coded_rpc) == bit_length // 8, f"{self.short_name} can't encode: Actual length is {len(coded_rpc)}, computed byte length is {bit_length // 8}, computed_rpc is {coded_rpc.hex()}, \n" + '\n'.join(
                self.__message_format_lines())

        return bytearray(coded_rpc)

    def convert_physical_to_bytes(self, param_values: dict, encode_state: EncodeState, bit_position=0):
        if bit_position != 0:
            raise EncodeError("Structures must be aligned, i.e. bit_position=0, but "
                              f"{self.short_name} was passed the bit position {bit_position}")
        return self.convert_physical_to_internal(param_values,
                                                 triggering_coded_request=encode_state.triggering_request,
                                                 is_end_of_pdu=encode_state.is_end_of_pdu
                                                 )

    def convert_bytes_to_physical(self, decode_state: DecodeState, bit_position=0):
        if bit_position != 0:
            raise DecodeError("Structures must be aligned, i.e. bit_position=0, but "
                              f"{self.short_name} was passed the bit position {bit_position}")
        byte_code = decode_state.coded_message[decode_state.next_byte_position:]
        inner_decode_state = DecodeState(coded_message=byte_code,
                                         parameter_value_pairs=[],
                                         next_byte_position=0)

        for parameter in self.parameters:
            value, next_byte_position = parameter.decode_from_pdu(
                inner_decode_state)

            inner_decode_state.parameter_value_pairs.append(
                ParameterValuePair(parameter, value))
            inner_decode_state = DecodeState(coded_message=byte_code,
                                             parameter_value_pairs=inner_decode_state.parameter_value_pairs,
                                             next_byte_position=max(inner_decode_state.next_byte_position,
                                                                    next_byte_position))
        # Construct the param dict.
        # TODO: Wouldn't it be prettier if we kept the information of each parameter
        #       instead of just using the short_name as the key and "forgetting" everything else?
        # old version
        # param_dict = OrderedDict((pv.parameter.short_name, pv.value) for pv in inner_decode_state.parameter_value_pairs)
        # new version by Barry
        param_dict = []
        for pv in inner_decode_state.parameter_value_pairs:
            param_dict.append(OrderedDict[pv.parameter.short_name, pv.value])

        return param_dict, decode_state.next_byte_position + inner_decode_state.next_byte_position

    def encode(self, coded_request=None, **params) -> bytearray:
        """
        Composes an UDS message as bytes for this service.
        Parameters:
        ----------
        coded_request: bytes
            coded request (only needed when encoding a response)
        params: dict
            Parameters of the RPC as mapping from SHORT-NAME of the parameter to the value
        """
        return self.convert_physical_to_internal(params,
                                                 triggering_coded_request=coded_request,
                                                 is_end_of_pdu=True)

    def decode(self, message: Union[bytes, bytearray]):
        # dummy decode state to be passed to convert_bytes_to_physical
        decode_state = DecodeState(coded_message=message,
                                   parameter_value_pairs=[],
                                   next_byte_position=0)
        param_values, next_byte_position = self.convert_bytes_to_physical(
            decode_state)
        if len(message) != next_byte_position:
            raise DecodeError(
                f"The message {message.hex()} is longer than could be parsed. Expected {next_byte_position} but got {len(message)}.")
        return param_values

    def parameter_dict(self):
        """
        Returns a dict with parameter short names as keys.
        The values are parameters for simple types or a nested dict for structures.
        """
        params = self.parameters
        assert all(not isinstance(p, ParameterWithDOP) or isinstance(
            p.dop, DataObjectProperty) or isinstance(p.dop, Structure) for p in self.parameters)
        param_dict: Dict[str, Union[Parameter, Dict[str, Parameter]]] = {
            p.short_name: p for p in params
            if not isinstance(p, ParameterWithDOP) or not isinstance(p.dop, Structure)
        }
        param_dict.update({
            struct_param.short_name: struct_param.dop.parameter_dict()
            for struct_param in params if isinstance(struct_param, ParameterWithDOP) and isinstance(struct_param.dop, BasicStructure)
        })
        return param_dict

    def _resolve_references(self, parent_dl, id_lookup):
        """Recursively resolve any references (odxlinks or sn-refs)
        """
        for p in self.parameters:
            if isinstance(p, ParameterWithDOP):
                p.resolve_references(parent_dl, id_lookup)

    def __message_format_lines(self, allow_unknown_lengths=False):
        # sort parameters
        sorted_params: list = list(self.parameters)  # copy list
        if all(p.byte_position is not None for p in self.parameters):
            sorted_params.sort(key=lambda p: (
                p.byte_position, 8 - p.bit_position))

        # replace structure parameters by their sub parameters
        params = []
        for p in sorted_params:
            if isinstance(p, ValueParameter) and isinstance(p.dop, BasicStructure):
                params += p.dop.parameters
            else:
                params.append(p)

        i = 0
        byte = 0
        # needs to be one larger than the maximum digit length of a byte number
        indent_for_byte_numbering = 5 * " "
        formatted_lines = [indent_for_byte_numbering +
                           "".join(f"   {7-bit}  " for bit in range(8))]

        breakpoint = 0  # absolute bit position where the next parameter starts

        divide_string = indent_for_byte_numbering + 8 * "+-----" + "+"

        error = False
        next_line = ""
        while i <= len(params) and not error:  # For each byte
            if 8 * byte == breakpoint and i == len(params):
                # If we have formatted the last parameter, we're done.
                break

            formatted_lines.append(f"{divide_string}")
            if breakpoint // 8 - byte > 5:
                curr_param = params[i-1].short_name
                formatted_lines.append(
                    indent_for_byte_numbering + f"  ... {breakpoint // 8 - byte} bytes belonging to {curr_param} ... ")
                byte += breakpoint // 8 - byte
                continue

            next_line = f"{(len(indent_for_byte_numbering) - 1 - len(str(byte))) * ' '}{byte} "

            for bit in range(8):
                assert 8 * byte + bit <= breakpoint

                if 8 * byte + bit == breakpoint:
                    # END-OF-PDU fields do not exhibit a fixed bit
                    # length, so they need special treatment here
                    dct = None
                    if hasattr(params[i], 'dop'):
                        dop = params[i].dop
                        if hasattr(dop, 'diag_coded_type'):
                            dct = dop.diag_coded_type

                    if dct is not None and dct.dct_type == 'MIN-MAX-LENGTH-TYPE':
                        name = params[i].short_name + " ("
                        if dct.termination == "END-OF-PDU":
                            name += "End of PDU, "
                        name += f"{dct.min_length}..{dct.max_length} bytes"
                        name += ")"
                        next_line += "| " + name

                        i += 1

                        # adding 8 is is a bit hacky here, but hey, it
                        # works ...
                        breakpoint += 8

                        break

                    elif not params[i].bit_length and not allow_unknown_lengths:
                        # The bit length is not set for the current
                        # parameter, i.e. it was either not specified
                        # or the parameter is of variable length and
                        # has an type which is not handled above. In
                        # this case, stop trying.
                        error = True
                        break
                    else:
                        breakpoint += params[i].bit_length or (
                            allow_unknown_lengths and 8)
                        name = params[i].short_name + \
                            f" ({params[i].bit_length or 'Unknown'} bits)"
                        next_line += "| " + name

                    i += 1

                    if byte == breakpoint // 8:
                        char_pos = bit * 6 + 2 + len(name)
                        width_of_line = (breakpoint % 8) * 6
                        if char_pos < width_of_line:
                            next_line += " " * \
                                (width_of_line - char_pos) + "|"
                        # start next line (belongs to same byte)
                        formatted_lines.append(next_line)
                        # fill next line with white spaces upto the bit where next parameter starts
                        next_line = indent_for_byte_numbering + \
                            (bit + 1) * 6 * " "
                    else:
                        char_pos = 2 + bit * 6 + len(name)
                        width_of_line = 8 * 6
                        if char_pos < width_of_line:
                            next_line += " " * \
                                (width_of_line - char_pos) + "|"
                        break
                else:
                    if bit == 0:
                        next_line += "|" + 5 * " "
                    elif bit == 7:
                        next_line += 6 * " " + "|"
                    else:
                        next_line += 6 * " "

            formatted_lines.append(next_line)
            next_line = ""

            byte += 1

        if not error:
            formatted_lines.append(divide_string)
            return formatted_lines
        else:
            return None

    def print_message_format(self, indent: int = 5, allow_unknown_lengths=False):
        """
        Print a description of the message format to `stdout`.
        """

        message_as_lines = self.__message_format_lines(
            allow_unknown_lengths=allow_unknown_lengths)
        if message_as_lines is not None:
            print(f"{indent * ' '}" +
                  f"\n{indent * ' '}".join(message_as_lines))
        else:
            print("Sorry, couldn't pretty print message layout. :(")
        for p in self.parameters:
            print(indent * ' ' +
                  str(p).replace("\n", f"\n{indent * ' '}"))


class Structure(BasicStructure):
    def __init__(self, id, short_name, parameters, long_name=None, byte_size=None, description=None):
        super().__init__(id, short_name, parameters,
                         long_name=long_name, description=description)

        self.parameters = parameters
        self.basic_structure = BasicStructure(id, short_name, parameters,
                                              long_name=long_name, byte_size=byte_size, description=description)

    def __repr__(self) -> str:
        return f"Structure('{self.short_name}', byte_size={self._byte_size})"

    def __str__(self) -> str:
        params = "[\n" + "\n".join([" " + str(p).replace("\n", "\n ")
                                   for p in self.parameters]) + "\n]"

        return \
            f"Structure '{self.short_name}': " + \
            f"Byte size={self._byte_size}, " + \
            f"Parameters={params}"


class Request(BasicStructure):
    def __init__(self, id, short_name, parameters, long_name=None, description=None):
        super().__init__(id, short_name, parameters,
                         long_name=long_name, description=description)

    def __repr__(self) -> str:
        return f"Request('{self.short_name}')"

    def __str__(self) -> str:
        return f"Request('{self.short_name}')"


class Response(BasicStructure):
    def __init__(self, id, short_name, parameters, long_name=None, response_type=None, description=None):
        super().__init__(id, short_name, parameters,
                         long_name=long_name, description=description)
        self.response_type = "POS-RESPONSE" if response_type == "POS-RESPONSE" else "NEG-RESPONSE"

    def encode(self, coded_request: bytearray = None, **params):
        logger.info(f"Compose response message to the request {coded_request}")
        if coded_request is not None:
            # Extract MATCHING-REQUEST-PARAMs from the coded request
            for param in self.parameters:
                if param.parameter_type == "MATCHING-REQUEST-PARAM":
                    logger.info(
                        f"set matching request param value {param.short_name}")
                    byte_pos = param.request_byte_position
                    byte_length = param.byte_length

                    val = coded_request[byte_pos:byte_pos+byte_length]
                    params[param.short_name] = val

        return super().encode(coded_request=coded_request, **params)

    def __repr__(self) -> str:
        return f"Response('{self.short_name}')"

    def __str__(self) -> str:
        return f"Response('{self.short_name}')"


def read_structure_from_odx(et_element) -> Union[Structure, Request, Response, None]:
    id = et_element.get("ID")
    short_name = et_element.find("SHORT-NAME").text
    long_name = et_element.find("LONG-NAME")
    if long_name is not None:
        long_name = long_name.text
    description = read_description_from_odx(et_element.find("DESC"))
    parameters = [read_parameter_from_odx(et_parameter)
                  for et_parameter in et_element.iterfind("PARAMS/PARAM")]

    res: Union[Structure, Request, Response, None]
    if et_element.tag == "REQUEST":
        res = Request(
            id,
            short_name,
            parameters=parameters,
            long_name=long_name,
            description=description
        )
    elif et_element.tag in ["POS-RESPONSE", "NEG-RESPONSE"]:
        res = Response(
            id,
            short_name,
            response_type=et_element.tag,
            parameters=parameters,
            long_name=long_name,
            description=description
        )
    elif et_element.tag == "STRUCTURE":
        byte_size = int(et_element.find(
            "BYTE-SIZE").text) if et_element.find("BYTE-SIZE") is not None else None
        res = Structure(
            id,
            short_name,
            parameters=parameters,
            byte_size=byte_size,
            long_name=long_name,
            description=description
        )
    else:
        res = None
        logger.critical(
            f"Did not recognize structure {et_element.tag} {short_name}")
    return res
