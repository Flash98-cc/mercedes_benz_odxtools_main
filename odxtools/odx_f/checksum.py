# created by Barry at 2022.06.22
# P262 has a demo structure
from dataclasses import dataclass
from ..odxtypes import DataType
from ..diaglayer import read_short_name


@dataclass()
class CheckSum_Result:
    type: DataType = None
    content: str = None


def read_checksum_result(et_element):
    if et_element is None:
        return None
    type = et_element.get("TYPE")
    content = et_element.text
    return CheckSum_Result(type, content)


# TODO: CHECKSUM is not defined for now
@dataclass()
class CheckSum:
    id: str = None
    short_name: str = None
    # TODO: fillbyte, source_start_address, source_end_address are hexBinary type, how to define it?
    fillbyte = None
    source_start_address = None
    source_end_address = None
    checksum_alg: str = None
    compressed_size: int = None
    uncompressed_size: int = None
    checksum_result: CheckSum_Result = None


def read_checksum_from_odx(et_element):
    if et_element is None:
        return None
    id = et_element.get("ID")
    short_name = read_short_name(et_element.find("SHORT-NAME"))
    fillbyte = et_element.find("FILLBYTE").text
    source_start_address = et_element.find("SOURCE-START-ADDRESS").text
    checksum_alg = et_element.find("CHECKSUM-ALG").text
    # source_end_address and uncompressed_size is xor relationship
    checksum_result = read_checksum_result(et_element.find("CHECKSUM-RESULT"))
    if et_element.find("SOURCE-END-ADDRESS") is not None:
        source_end_address = et_element.find("SOURCE-END-ADDRESS").text
    return CheckSum(id=id,
                    short_name=short_name,
                    fillbyte=fillbyte,
                    source_start_address=source_start_address,
                    source_end_address=source_end_address,
                    checksum_alg=checksum_alg,
                    compressed_size=None,
                    uncompressed_size=None,
                    checksum_result=checksum_result
                    )

