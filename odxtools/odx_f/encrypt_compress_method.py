# created by Barry at 2022.06.22
from ..globals import xsi
from dataclasses import dataclass


# <ENCRYPT-COMPRESS-METHOD TYPE="A_UINT32">33</ENCRYPT-COMPRESS-METHOD> in page 247
@dataclass()
class Encrypt_Compress_Method:
    # type: Union["A_UINT32", "A_BYTEFIELD"]
    type: str = None

    content: str = None


def read_encrypt_compress_method(et_element):
    if et_element is None:
        return None
    type = et_element.get(f"{xsi}type")
    content = et_element.text
    return Encrypt_Compress_Method(type, content)

