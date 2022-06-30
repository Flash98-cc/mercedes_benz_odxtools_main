# encoding: utf-8
# -*- coding: UTF-8 -*-
from cgitb import enable
from itertools import chain
from pickle import FALSE
from typing import Type
from odxtools import admindata, diaglayer
from odxtools.database import Database
from zipfile import ZipFile
import odxtools
from odxtools.load_file import load_file

# load a odx-f file
# filepath = r"D:\PDX\DTS_Example\ECMFlashSpec.odx-f"
# db = load_file(file_name=filepath, enable_candela_workarounds=False)
# print("Debug")

# load a odx-v file
# filepath = r"D:\PDX\Sample\Vehicle_Info_Spec.odx-v"
# db = load_file(file_name=filepath, enable_candela_workarounds=False)
# print("Debug")

# load a odx-cs file
# filepath = r"D:\PDX\Sample\ISO_15765_3.odx-cs"
# db = load_file(file_name=filepath, enable_candela_workarounds=False)
# print("Debug")

# load a odx-c file
# filepath = r"D:\PDX\Sample\UDSOnCAN_CPS.odx-c"
# db = odxtools.load_file(file_name=filepath, enable_candela_workarounds=False)
# print("Debug")

# load a odx-d file
# filepath = r"D:\PDX\Sample\FG_UDS.odx-d"
# db = load_file(file_name=filepath, enable_candela_workarounds=False)
# print("Debug")

# load a pdx file
# filepath = r"D:\PDX\DTS_Example.pdx"
# db = load_file(file_name=filepath, enable_candela_workarounds=False)
# print("Debug")

# load sample.pdx
filepath = r"D:\PDX\Sample.pdx"
db = load_file(file_name=filepath, enable_candela_workarounds=False)
print("Debug")
