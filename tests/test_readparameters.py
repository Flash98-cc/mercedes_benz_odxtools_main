# SPDX-License-Identifier: MIT
# Copyright (c) 2022 MBition GmbH

import unittest
from xml.etree import ElementTree

from odxtools.odxtypes import DataType
from odxtools.parameters import NrcConstParameter, read_parameter_from_odx


class TestReadNrcParam(unittest.TestCase):
    def test_read_nrcconst_from_odx(self):
        ODX = """
        <PARAM SEMANTIC="SUBFUNCTION-ID" xsi:type="NRC-CONST" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <SHORT-NAME>NR_identifier</SHORT-NAME>
            <LONG-NAME>Identifier for the negative response</LONG-NAME>
            <BYTE-POSITION>0</BYTE-POSITION>
            <CODED-VALUES>
                <CODED-VALUE>16</CODED-VALUE>
                <CODED-VALUE>10</CODED-VALUE>
            </CODED-VALUES>
            <DIAG-CODED-TYPE BASE-DATA-TYPE="A_UINT32" xsi:type="STANDARD-LENGTH-TYPE">
                <BIT-LENGTH>8</BIT-LENGTH>
            </DIAG-CODED-TYPE>
        </PARAM>
        """
        root = ElementTree.fromstring(ODX)
        param = read_parameter_from_odx(root)

        self.assertIsInstance(param, NrcConstParameter)
        self.assertEqual("SUBFUNCTION-ID", param.semantic)
        self.assertEqual("NR_identifier", param.short_name)
        self.assertEqual("Identifier for the negative response",
                         param.long_name)
        self.assertEqual([16, 10], param.coded_values)
        self.assertEqual(DataType.A_UINT32,
                         param.diag_coded_type.base_data_type)
        self.assertEqual(8, param.diag_coded_type.bit_length)
