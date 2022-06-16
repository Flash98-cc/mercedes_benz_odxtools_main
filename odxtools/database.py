# SPDX-License-Identifier: MIT
# Copyright (c) 2022 MBition GmbH

from ast import Lambda
from ctypes import sizeof
from string import printable
from typing import Any, Dict, Type
from xml.etree import ElementTree
from itertools import chain
from zipfile import ZipFile

from .diaglayer import DiagLayer, read_diag_layer_container_from_odx
from .globals import logger
from .nameditemlist import NamedItemList
from .odx_c.comparamspec import Comparam_Spec, read_comparam_spec_from_odx  # 导入处理odx-c的文件
from .odx_cs.comparamsubset import read_comparam_subset_from_odx
from .odx_v.vehicle_info_spec import read_vehicle_info_spec_from_odx


class Database:
    """This class internalizes the diagnostic database for various ECUs
    described by a collection of ODX files which are usually collated
    into a single PDX file.
    """

    def __init__(self,
                 pdx_zip: ZipFile = None,
                 odx_file_name: str = None,
                 enable_candela_workarounds: bool = True):
        self._id_lookup: Dict[str, Any] = {}
        dlc_elements = []
        # self._chen = []
        if pdx_zip is None and odx_file_name is None:
            # create an empty database object
            return
        if pdx_zip is not None and odx_file_name is not None:  # pdx和odx不能同时出现，参数互斥
            raise TypeError("The 'pdx_zip' and 'odx_d_file_name' parameters are mutually exclusive")

        # 处理pdx文件
        if pdx_zip is not None:
            names = list(pdx_zip.namelist())
            names.sort()
            # 处理odx-d
            for zip_member in names:
                if zip_member.endswith(".odx-d"):  # 判断是不是odx-d文件
                    logger.info(f"Processing the file {zip_member}")
                    d = pdx_zip.read(zip_member)  # d是读入进来odx-d文件的string
                    root = ElementTree.fromstring(d)
                    logger.info(root)
                    dlc_elements.append(root.find("DIAG-LAYER-CONTAINER"))

            tmp = [
                read_diag_layer_container_from_odx(dlc_el, enable_candela_workarounds=enable_candela_workarounds) \
                for dlc_el in dlc_elements
            ]
            self._diag_layer_containers = NamedItemList(lambda x: x.short_name, tmp)

            self._diag_layer_containers.sort(key=lambda x: x.short_name)  # 按照short_name 排序
            self.finalize_init()

            # 处理odx-c
            # for zip_member in names:
            #    if zip_member.endswith(".odx-c"):
            #        d = pdx_zip.read(zip_member)
            #        root = ElementTree.fromstring(d)
            #        dlc_elements.append(root.find("COMPARAM-SPEC"))
            # tmp = [
            #        read_comparam_spec_from_odx(dlc_el, enable_candela_workarounds=enable_candela_workarounds) \
            #            for dlc_el in dlc_elements
            #      ]
            # print("test")

            # 处理单个odx-d 文件
        elif odx_file_name is not None:
            if odx_file_name.endswith(".odx-d"):
                dlc_element = ElementTree.parse(odx_file_name).find("DIAG-LAYER-CONTAINER")
                self._diag_layer_containers = \
                    NamedItemList(lambda x: x.short_name,
                                  [read_diag_layer_container_from_odx(dlc_element)])
                self.finalize_init()
            # 处理单个odx-c文件
            elif odx_file_name.endswith(".odx-c"):
                dlc_element = ElementTree.parse(odx_file_name).find("COMPARAM-SPEC")
                self._comparam_spec = \
                    NamedItemList(lambda x: x.short_name,
                                  [read_comparam_spec_from_odx(dlc_element)])
            # 处理单个odx-cs 文件
            elif odx_file_name.endswith(".odx-cs"):
                dlc_element = ElementTree.parse(odx_file_name).find("COMPARAM-SUBSET")
                self._comparam_subset = \
                    NamedItemList(lambda x: x.short_name,
                                  [read_comparam_subset_from_odx(dlc_element)])
            # 处理单个odx-v 文件
            elif odx_file_name.endswith(".odx-v"):
                dlc_element = ElementTree.parse(odx_file_name).find("VEHICLE-INFO-SPEC")
                self._vehicle_info_spec = \
                    NamedItemList(lambda x: x.short_name,
                                  [read_vehicle_info_spec_from_odx(dlc_element)])

    def finalize_init(self):
        # Create wrapper objects
        # modified by cc at 18:01 2022/5/25
        # for dlc in self.diag_layer_containers:
        #    print("the type of dlc: ", type(dlc))
        # modified by cc at 18:01 2022/5/25

        self._diag_layers = NamedItemList(
            lambda dl: dl.short_name, chain(*(dlc.diag_layers for dlc in self.diag_layer_containers)))
        self._ecus = NamedItemList(
            lambda ecu: ecu.short_name, chain(*(dlc.ecu_variants for dlc in self.diag_layer_containers)))

        # Build id_lookup
        self._id_lookup = {}  # dict

        for dlc in self.diag_layer_containers:
            self.id_lookup.update(dlc._build_id_lookup())
            # self.id_lookup返回一个dict，使用update将新的键值对更新到self._id_lookup中
        for dl in self.diag_layers:
            self.id_lookup.update(dl._build_id_lookup())

        # Resolve references
        """ for dlc in self.diag_layer_containers:
            dlc._resolve_references(self.id_lookup)
 """
        for dl_type_name in ["ECU-SHARED-DATA", "PROTOCOL", "FUNCTIONAL-GROUP", "BASE-VARIANT", "ECU-VARIANT"]:
            for dl in self.diag_layers:
                if dl.variant_type == dl_type_name:
                    dl._resolve_references(self.id_lookup)

    @property
    def id_lookup(self) -> dict:
        """A map from id to object"""
        return self._id_lookup

    @property
    def ecus(self) -> NamedItemList[DiagLayer]:
        """ECU-variants defined in the data base"""
        return self._ecus

    @property
    def diag_layers(self) -> NamedItemList[DiagLayer]:
        """all diagnostic layers defined in the data base"""
        return self._diag_layers

    @property
    def diag_layer_containers(self):
        return self._diag_layer_containers

    # modifu value
    @diag_layer_containers.setter
    def diag_layer_containers(self, value):
        self._diag_layer_containers = value

    @property
    def comparam_spec(self):
        return self._comparam_spec

    @property
    def comparam_subset(self):
        return self._comparam_subset

    @property
    def vehicle_info_spec(self):
        return self._vehicle_info_spec
