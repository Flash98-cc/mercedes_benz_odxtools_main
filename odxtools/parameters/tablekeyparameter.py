# SPDX-License-Identifier: MIT
# Copyright (c) 2022 MBition GmbH


from .parameterbase import Parameter


# used for reading and writing data by data identifier(DID)
# for more details, see 7.3.6.11
class TableKeyParameter(Parameter):
    def __init__(self,
                 short_name,
                 table_ref=None,
                 table_snref=None,
                 table_row_snref=None,
                 table_row_ref=None,
                 id=None,
                 long_name=None,
                 byte_position=None,
                 bit_position=0,
                 semantic=None,
                 description=None):
        super().__init__(
            short_name=short_name,
            long_name=long_name,
            byte_position=byte_position,
            bit_position=bit_position,
            parameter_type="TABLE-KEY",
            semantic=semantic,
            description=description
        )
        if table_ref:
            self.table_ref = table_ref
            self.table_row_snref = table_row_snref
        elif table_snref:
            self.table_ref = table_ref
            self.table_row_snref = table_row_snref
        elif table_row_ref:
            self.table_row_ref = table_row_ref
        else:
            raise ValueError(
                "Either table_key_ref or table_key_snref must be defined.")
        self.id = id

    def is_required(self):
        raise NotImplementedError(
            "TableKeyParameter.is_required is not implemented yet.")

    def is_optional(self):
        raise NotImplementedError(
            "TableKeyParameter.is_optional is not implemented yet.")

    def get_coded_value(self):
        raise NotImplementedError(
            "Encoding a TableKeyParameter is not implemented yet.")

    def get_coded_value_as_bytes(self):
        raise NotImplementedError(
            "Encoding a TableKeyParameter is not implemented yet.")

    def decode_from_pdu(self, coded_message, default_byte_position=None):
        raise NotImplementedError(
            "Decoding a TableKeyParameter is not implemented yet.")
