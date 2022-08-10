# encoding: utf-8
# -*- coding: UTF-8 -*-
from cgitb import enable
from itertools import chain
from pickle import FALSE
from typing import Type, Optional


from odxtools import admindata, diaglayer
from odxtools.database import Database
from zipfile import ZipFile
import odxtools
from odxtools.load_file import load_file


def getDatabase():
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
    # filepath = r"D:\PDX\Sample.pdx"
    # db = load_file(file_name=filepath, enable_candela_workarounds=False)
    # print("Debug")

    # Get CAN ID
    database = odxtools.load_pdx_file(r"D:\PDX\Sample.pdx", enable_candela_workarounds=False)
    print("Return an UDS_on_CAN database")
    return database


#  return some parameters
def return_cp_buadrate(self, shortname: str) -> Optional[str]:
    if shortname is None:
        return None
    else:
        return self.db


db = getDatabase()
print("debug odx database")


def getPinNumber():
    """
    return UDS_on_CAN PIN Number
    """
    can_low: int = 0
    can_high: int = 0
    for vehicle_info_spec in db.vehicle_info_specs:
        for vehicle_information in vehicle_info_spec.vehicle_informations:
            logical_link = vehicle_information.logical_links[2]
            vehicle_connector_pin_refs = logical_link.physical_vehicle_link_ref.physical_vehicle_link.vehicle_connector_pin_refs
            for vehicle_connector_pin_ref in vehicle_connector_pin_refs:
                if vehicle_connector_pin_ref.vehicle_connector_pin.short_name.find("HIGH") >= 0:
                    can_high = vehicle_connector_pin_ref.vehicle_connector_pin.pin_number
                elif vehicle_connector_pin_ref.vehicle_connector_pin.short_name.find("LOW") >= 0:
                    can_low = vehicle_connector_pin_ref.vehicle_connector_pin.pin_number
    # return int(can_high), int(can_low)
    return {'can_high': can_high, 'can_low': can_low}


def get_UDS_on_CAN_11898_2_DWCAN_Parameters():
    parameter: dict[str, str] = {}
    for vehicle_info_spec in db.vehicle_info_specs:
        for vehicle_information in vehicle_info_spec.vehicle_informations:
            logical_link = vehicle_information.logical_links[2]
            #
            prot_stack = logical_link.protocol_ref.protocol.comparam_spec_ref.comparam_spec.prot_stacks[0]
            comparam_subset_refs = prot_stack.comparam_subset_refs
            for comparam_subset_ref in comparam_subset_refs:
                comparamsubset = comparam_subset_ref.comparamsubset
                comparams = comparamsubset.comparams
                complex_comparams = comparamsubset.complex_comparams

                for comparam in comparams:
                    if comparam.physical_default_value is not None:
                        parameter[comparam.short_name] = comparam.physical_default_value

                for complex_comparm in complex_comparams:
                    for comparam in complex_comparm.comparams:
                        if comparam.physical_default_value is not None:
                            parameter[comparam.short_name] = comparam.physical_default_value
    return parameter


# rerurn a UniqueRespIdTable in ISO-15765-2 Complex-comparams
def get_Unique_Resp_Id_Table():
    parameter: dict[str, str] = {}
    for comparam_subset in db.comparam_subsets:
        if comparam_subset.short_name == "ISO_15765_2":
            comparams = comparam_subset.complex_comparams[0].comparams
            for comparam in comparams:
                parameter[comparam.short_name] = comparam.physical_default_value
    return parameter


# if __name__ == "__main__":
#     newdict = get_Unique_Resp_Id_Table()
#     print("test")

