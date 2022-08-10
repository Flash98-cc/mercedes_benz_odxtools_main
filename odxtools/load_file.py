# SPDX-License-Identifier: MIT
# Copyright (c) 2022 MBition GmbH

from .load_pdx_file import load_pdx_file
from .load_odx_d_file import load_odx_d_file
from .load_odx_c_file import load_odx_c_file
from .load_odx_cs_file import load_odx_cs_file
from .load_odx_v_file import load_odx_v_file
from .load_odx_f_file import load_odx_f_file


def load_file(file_name: str, enable_candela_workarounds: bool = True):
    if file_name.lower().endswith(".pdx"):
        return load_pdx_file(pdx_file=file_name, enable_candela_workarounds=enable_candela_workarounds)
    elif file_name.lower().endswith(".odx-d"):
        return load_odx_d_file(odx_d_file_name=file_name, enable_candela_workarounds=enable_candela_workarounds)
    elif file_name.lower().endswith(".odx-c"):
        return load_odx_c_file(odx_c_file_name=file_name, enable_candela_workarounds=enable_candela_workarounds)
    elif file_name.lower().endswith(".odx-cs"):
        return load_odx_cs_file(odx_cs_file_name=file_name, enable_candela_workarounds=enable_candela_workarounds)
    elif file_name.lower().endswith(".odx-v"):
        return load_odx_v_file(odx_v_file_name=file_name, enable_candela_workarounds=enable_candela_workarounds)
    elif file_name.lower().endswith(".odx-f"):
        return load_odx_f_file(odx_f_file_name=file_name, enable_candela_workarounds=enable_candela_workarounds)
    else:
        raise RuntimeError(f"Could not guess the file format of file '{file_name}'!")
