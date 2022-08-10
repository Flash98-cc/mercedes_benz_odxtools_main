# created by Barry at 2022.06.21
# see p250 for more details
from dataclasses import dataclass
from ..globals import xsi
from .encrypt_compress_method import Encrypt_Compress_Method, read_encrypt_compress_method
from .dataformat import DataFormat, read_dataformat_from_flashdata
from ..utils import read_description_from_odx


# only when FLASHDATA TYPE is EXTERN-FLASHDATA, this element works
@dataclass()
class Datafile:
    latebound_datafile: bool = None
    content: str = None


def read_datafile(et_element):
    if et_element is None:
        return None
    latebound_datafile = et_element.get("LATEBOUND-DATAFILE")
    content = et_element.text
    return Datafile(latebound_datafile, content)


@dataclass()
class Flashdata:
    id: str = None
    oid: str = None
    ##  type: Union["INTERN-FLASHDATA", "EXTERN-FLASHDATA"]

    short_name: str = None
    long_name: str = None
    description: str = None
    # SIZE-LENGTH and ADDRESS-LENGTH belong to element FLASHDATA
    # describle the parameters LengthOfMemorySize of the service "requestDownload" in ISO14229-1
    size_length: int = None
    address_length: int = None

    encrypt_compress_method: Encrypt_Compress_Method = None
    dataformat: DataFormat = None
    type: str = None
    # INTERN-FLASHDATA WORKS
    # the D-server shall convert all pairs of hexadecimal digits to a byte stream at first
    data: str = None
    # EXTERN-FLASHDATA WORKS
    # the xml format is not intended to hold giant data, therefore,
    datafile: Datafile = None


def read_flashdata_from_mem(et_element):
    id = et_element.get("ID")
    oid = et_element.get("OID") if et_element.get("OID") is not None else None
    short_name = et_element.find("SHORT-NAME").text if et_element.find("SHORT-NAME") is not None else None
    long_name = et_element.find("LONG-NAME").text if et_element.find("LONG-NAME") is not None else None
    description = read_description_from_odx(et_element.find("DESC"))
    size_length = et_element.find("SIZE-LENGTH").text if et_element.find("SIZE-LENGTH") is not None else None
    address_length = et_element.find("ADDRESS-LENGTH").text if et_element.find("ADDRESS-LENGTH") is not None else None

    dataformat = read_dataformat_from_flashdata(et_element.find("DATAFORMAT"))
    encrypt_compress_method = read_encrypt_compress_method(et_element.find("ENCRYPT-COMPRESS-METHOD"))

    type = et_element.get(f"{xsi}type")
    if type == "INTERN-FLASHDATA":
        data = et_element.find("DATA").text
        return Flashdata(id=id,
                         oid=oid,
                         short_name=short_name,
                         long_name=long_name,
                         description=description,
                         size_length=size_length,
                         address_length=address_length,
                         encrypt_compress_method=encrypt_compress_method,
                         dataformat=dataformat,
                         type=type,
                         data=data,
                         datafile=None
                         )
    elif type == "EXTERN-FLASHDATA":
        datafile = read_datafile(et_element.find("DATAFILE"))
        return Flashdata(id=id,
                         oid=oid,
                         short_name=short_name,
                         long_name=long_name,
                         description=description,
                         size_length=size_length,
                         address_length=address_length,
                         encrypt_compress_method=encrypt_compress_method,
                         dataformat=dataformat,
                         type=type,
                         data=None,
                         datafile=datafile)
