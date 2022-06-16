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

import xml.etree.ElementTree
from odxtools.__main__ import _main
from odxtools.diaglayer import DiagLayer

# load a odx-v file
filepath = r"D:\PDX\Sample\Vehicle_Info_Spec.odx-v"
db = load_file(file_name=filepath, enable_candela_workarounds=False)
print("hello")

# load a odx-cs file
# filepath = r"D:\PDX\Sample\ISO_15765_3.odx-cs"
# db = load_file(file_name=filepath, enable_candela_workarounds=False)
# print("hello")

# load a odx-c file
# filepath = r"D:\PDX\Sample\UDSOnCAN_CPS.odx-c"
# db = odxtools.load_file(file_name=filepath, enable_candela_workarounds=False)
# print("hello")


# 打印日志信息
# import logging
# logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s -%(levelname)s -%(message)s')
# logger=logging.getLogger(__name__)

# load pdx file db = odxtools.load_pdx_file(pdx_file =
# r"D:\ATYC\GithubDemo\mercedes-benz_odxtools-main\TestCode\somersault.pdx",enable_candela_workarounds=False) print(
# f" get data ") load new pdx file which's odx-d file has DTC db = odxtools.load_pdx_file(pdx_file =
# r"D:\udsoncan.pdx",enable_candela_workarounds = False) db = odxtools.load_pdx_file(pdx_file = r"D:\PDX\Sample\",
# enable_candela_workarounds=False) #为何只有somersault.pdx才可以解析，其他名字都无法解析


# load a odx-d file as input file
# db = odxtools.load_odx_d_file(odx_d_file_name = r"D:\somersault.odx-d", enable_candela_workarounds = False)
# db = odxtools.load_odx_d_file(odx_d_file_name = "D:\somersault2.odx-d",enable_candela_workarounds = False)
print(f" this udsoncan ")
# 打印somersault_lazy 的ecu name 和 ecu 提供的services
# ecu = db.ecus.somersault_lazy        #db.ecus下面有两个ecu，分别是somersault_lazy 和somersault_assiduous
# print(f"Available services for {ecu.short_name}:{ecu.services}")

# 获取diag_layer_container里面部分内容
# for odx_d_list in db.diag_layer_containers:
#    print(odx_d_list.admin_data,"\n") #打印admin_data
#    for docrevision in odx_d_list.admin_data.doc_revisions:
#        print(docrevision,"\n") #打印admin_data 的doc_revisions
#    for ecu_variant in odx_d_list.ecu_variants:
#        print(ecu_variant) #打印ecu_variant

#
# ecus = db.ecus
# i = 0
# for ecu in ecus:
#    for compar in ecu.communication_parameters:
#        print(f"{compar.id_ref} : {compar.value} ")

# 获取data_object_properties(DOP)中dtc
# diag_layer_containers = db.diag_layer_containers
# for diag_layer_container in diag_layer_containers: #somersault 层
#    for Diag_layer in chain(diag_layer_container.base_variants, 
#                      diag_layer_container.ecu_shared_datas,
#                      diag_layer_container.ecu_variants,
#                      diag_layer_container.functional_groups,
#                      diag_layer_container.protocols):
#        dops = Diag_layer.data_object_properties #获得data object properity
#        for dop in dops:
#            if hasattr(dop,'dtcs'): #判断当前dop有无dtc属性 
#                print(dop.dtcs)


"""
#决定发送和接受诊断信息的CAN ID
print(f"ECU {ecu.short_name} listens for requests on CAN ID 0x{ecu.get_receive_id():x}")
print(f"ECU {ecu.short_name} transmits responses on CAN ID 0x{ecu.get_send_id():x}")

#Encode a session_start request to the somerasult_lazy ECU
raw_request_data = ecu.services.session_start()
print(f"Message for session start request of ECU {ecu.short_name} : {raw_request_data}") """

""" raw_request_data = ecu.services.session_start()
raw_response_data = ecu.services.session_start.positive_responses[0].encode(coded_request=raw_request_data)
print("Positive response to session_start() of ECU {ecu.short_name}: {raw_response_data}") """
# -> bytearray(b'P')

""" #Decode a request
raw_data = b"\x10\x00"
decoded_message = ecu.decode(raw_data)
print(f"decoded message: {decoded_message}")

#Decode a response to a request
raw_request_data = b"\x10\x00"
raw_response_data = b'p'
decoded_response = ecu.decode_response(raw_response_data,raw_request_data)
print(f"decoded response : {decoded_response}")
 """
