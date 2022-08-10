# created by Barry at 2022.06.22

from dataclasses import dataclass
from ..odxtypes import DataType


@dataclass()
class Segment:
    def __init__(self,
                 id: str = None,
                 oid: str = None,
                 short_name: str = None,
                 long_name: str = None,
                 # the relationship between them
                 # uncompressed_size = source_start_address - source_end_address + 1
                 # source_end_address = source_start_address + uncompressed_size - 1
                 # source_start_address: DataType.A_BYTEFIELD = None,
                 # source_end_address: DataType.A_BYTEFIELD = None,
                 source_start_address: str = None,
                 source_end_address: str = None,
                 # compress_size 是实际要传输的flash-data 长度
                 # uncompress_size 是经过解密或者解压缩之后的数据长度，默认两者一样
                 compressed_size: str = None,
                 uncompressed_size: str = None,
                 # this is an optional element, specifes the encryption and compression algorithm used for the segment
                 # encrypt_compress_method: UNKNOWN STRUCTURE
                 ):
        self.id = id
        self.oid = oid
        self.short_name = short_name
        self.long_name = long_name
        self.source_start_address = source_start_address
        self.source_end_address = source_end_address
        self.uncompressed_size = uncompressed_size
        self.compressed_size = compressed_size
        print(f"self.source_start_address is {self.source_start_address}")
        print(f"self.source_end_address is {self.source_end_address}")
        # if self.source_end_address is not None:
        #     self.uncompressed_size = self.source_end_address - self.source_start_address + 1
        # if self.uncompressed_size is not None:
        #     self.source_end_address = self.uncompressed_size + self.source_start_address - 1


def read_segment_from_datablock(et_element):
    if et_element is None:
        return None
    id = et_element.get("ID")
    oid = et_element.get("OID") if et_element.get("OID") is not None else None
    short_name = et_element.find("SHORT-NAME").text if et_element.find("SHORT-NAME") is not None else None
    long_name = et_element.find("LONG-NAME").text if et_element.find("LONG-NAME") is not None else None
    source_start_address = et_element.find("SOURCE-START-ADDRESS").text \
        if et_element.find("SOURCE-START-ADDRESS") is not None else None

    source_end_address = et_element.find("SOURCE-END-ADDRESS").text \
        if et_element.find("SOURCE-END-ADDRESS") is not None else None

    uncompressed_size = et_element.find("UNCOMPRESSED-SIZE").text \
        if et_element.find("UNCOMPRESSED-SIZE") is not None else None

    return Segment(id,
                   oid,
                   short_name,
                   long_name,
                   source_start_address,
                   source_end_address,
                   compressed_size=None,
                   uncompressed_size=uncompressed_size)

