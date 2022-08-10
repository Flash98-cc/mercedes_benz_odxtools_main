# created by Barry at 2022.6.22

from dataclasses import dataclass

from ..odxtypes import DataType


@dataclass()
class Security_Method:
    type: DataType = None
    content: str = None


def read_security_method_from_security(et_element):
    if et_element is None:
        return None
    type = et_element.get("TYPE")
    content = et_element.text
    return Security_Method(type, content)


@dataclass()
class Fw_CheckSum:
    type: DataType = None
    content: str = None


def read_fw_checksum_from_security(et_element):
    if et_element is None:
        return None
    type = et_element.get("TYPE")
    content = et_element.text
    return Fw_CheckSum(type, content)


@dataclass()
class Validity_For:
    type: DataType = None
    content: str = None


def read_Validity_For_from_security(et_element):
    if et_element is None:
        return None
    type = et_element.get("TYPE")
    content = et_element.text
    return Validity_For(type, content)


@dataclass()
class Fw_Signature:
    type: DataType = None
    content: str = None


def read_fw_signature_from_security(et_element):
    if et_element is None:
        return None
    type = et_element.get("TYPE")
    content = et_element.text
    return Fw_Signature(type, content)


@dataclass()
class Security:
    security_method: Security_Method = None
    fw_checksum: Fw_CheckSum = None
    validity_for: Validity_For = None
    fw_signature: Fw_Signature = None


def read_security_from_session(et_element):
    if et_element is None:
        return None

    security_method = read_security_method_from_security(et_element.find("SECURITY-METHOD"))
    fw_checksum = read_fw_checksum_from_security(et_element.find("FW-CHECKSUM"))
    validity_for = read_Validity_For_from_security(et_element.find("VALIDITY-FOR"))
    fw_signature = read_fw_signature_from_security(et_element.find("FW-SIGNATURE"))

    return Security(security_method,
                    fw_checksum,
                    validity_for,
                    fw_signature)
