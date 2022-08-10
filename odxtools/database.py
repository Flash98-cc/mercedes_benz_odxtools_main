# SPDX-License-Identifier: MIT
# Copyright (c) 2022 MBition GmbH

from typing import Any, Dict, Type
from xml.etree import ElementTree
from itertools import chain
from zipfile import ZipFile

from .diaglayer import DiagLayer, read_diag_layer_container_from_odx
from .globals import logger
from .nameditemlist import NamedItemList
from .odx_c.comparamspec import read_comparam_spec_from_odx  # 导入处理odx-c的文件
from .odx_cs.comparamsubset import read_comparam_subset_from_odx
from .odx_v.vehicle_info_spec import read_vehicle_info_spec_from_odx
from .odx_f.flash import read_flash_from_odx
from .parent_dl import Parent_Dl

class Database:
    """This class internalizes the diagnostic database for various ECUs
    described by a collection of ODX files which are usually collated
    into a single PDX file.
    """

    def __init__(self,
                 pdx_zip: ZipFile = None,
                 odx_file_name: str = None,
                 enable_candela_workarounds: bool = True):
        # id_lookup is used to resolve odxlink references
        self._id_lookup: Dict[str, Any] = {}
        # sn_lookup is uedse to resolve snref references
        self.sn_lookup = Parent_Dl()
        dlc_elements = []
        cs_elements = []
        cssubset_elements = []
        vis_elements = []
        flash_elements = []
        if pdx_zip is None and odx_file_name is None:
            # create an empty database object
            return
        if pdx_zip is not None and odx_file_name is not None:  # pdx和odx不能同时出现，参数互斥
            raise TypeError("The 'pdx_zip' and 'odx_d_file_name' parameters are mutually exclusive")

        # 处理pdx文件
        if pdx_zip is not None:
            names = list(pdx_zip.namelist())
            names.sort()
            for zip_member in names:
                if zip_member.endswith(('odx-d', 'odx-c', 'odx-cs', 'odx-f', 'odx-v', 'odx-m', 'odx-fd')):
                    # print(f"{zip_member} : TRUE")
                    if zip_member.endswith(".odx-d"):
                        data = pdx_zip.read(zip_member)
                        root = ElementTree.fromstring(data)
                        dlc_elements.append(root.find("DIAG-LAYER-CONTAINER"))
                    if zip_member.endswith("odx-c"):
                        data = pdx_zip.read(zip_member)
                        root = ElementTree.fromstring(data)
                        cs_elements.append(root.find("COMPARAM-SPEC"))
                    if zip_member.endswith("odx-cs"):
                        data = pdx_zip.read(zip_member)
                        root = ElementTree.fromstring(data)
                        cssubset_elements.append(root.find("COMPARAM-SUBSET"))
                    if zip_member.endswith(".odx-v"):
                        data = pdx_zip.read(zip_member)
                        root = ElementTree.fromstring(data)
                        vis_elements.append(root.find("VEHICLE-INFO-SPEC"))
                    if zip_member.endswith("odx-f"):
                        data = pdx_zip.read(zip_member)
                        root = ElementTree.fromstring(data)
                        flash_elements.append(root.find("FLASH"))

            tmp_dlc = [read_diag_layer_container_from_odx(dlc_el, enable_candela_workarounds=enable_candela_workarounds)
                       for dlc_el in dlc_elements]
            self._diag_layer_containers = NamedItemList(lambda x: x.short_name, tmp_dlc)
            self._diag_layer_containers.sort(key=lambda x: x.short_name)

            tmp_cs = [read_comparam_spec_from_odx(cs_el, enable_candela_workarounds=enable_candela_workarounds)
                      for cs_el in cs_elements]
            self._comparam_specs = NamedItemList(lambda x: x.short_name, tmp_cs)
            self._comparam_specs.sort(key=lambda x: x.short_name)

            tmp_cssubset = [
                read_comparam_subset_from_odx(cssubset_el, enable_candela_workarounds=enable_candela_workarounds)
                for cssubset_el in cssubset_elements]
            self._comparam_subsets = NamedItemList(lambda x: x.short_name, tmp_cssubset)
            self._comparam_subsets.sort(key=lambda x: x.short_name)

            tmp_vis = [read_vehicle_info_spec_from_odx(vis_el, enable_candela_workarounds=enable_candela_workarounds)
                       for vis_el in vis_elements]
            self._vehicle_info_specs = NamedItemList(lambda x: x.short_name, tmp_vis)
            self._vehicle_info_specs.sort(key=lambda x: x.short_name)

            tmp_flash = [read_flash_from_odx(flash_el, enable_candela_workarounds=enable_candela_workarounds)
                         for flash_el in flash_elements]
            self._flash = NamedItemList(lambda x: x.short_name, tmp_flash)
            self._flash.sort(key=lambda x: x.short_name)

            self.finalize_init()

            # 处理单个odx-d 文件
        elif odx_file_name is not None:
            self._diag_layer_containers = []
            self._comparam_specs = []
            self._comparam_subsets = []
            self._flash = []
            self._vehicle_info_specs = []

            if odx_file_name.endswith(".odx-d"):
                dlc_element = ElementTree.parse(odx_file_name).find("DIAG-LAYER-CONTAINER")
                self._diag_layer_containers = \
                    NamedItemList(lambda x: x.short_name,
                                  [read_diag_layer_container_from_odx(dlc_element)])
                self.finalize_init()
            # 处理单个odx-c文件
            elif odx_file_name.endswith(".odx-c"):
                dlc_element = ElementTree.parse(odx_file_name).find("COMPARAM-SPEC")
                self._comparam_specs = \
                    NamedItemList(lambda x: x.short_name,
                                  [read_comparam_spec_from_odx(dlc_element)])
                self.finalize_init()
            # 处理单个odx-cs 文件
            elif odx_file_name.endswith(".odx-cs"):
                dlc_element = ElementTree.parse(odx_file_name).find("COMPARAM-SUBSET")
                self._comparam_subsets = \
                    NamedItemList(lambda x: x.short_name,
                                  [read_comparam_subset_from_odx(dlc_element)])
                self.finalize_init()
            # 处理单个odx-v 文件
            elif odx_file_name.endswith(".odx-v"):
                dlc_element = ElementTree.parse(odx_file_name).find("VEHICLE-INFO-SPEC")
                self._vehicle_info_specs = \
                    NamedItemList(lambda x: x.short_name,
                                  [read_vehicle_info_spec_from_odx(dlc_element)])
                self.finalize_init()

            elif odx_file_name.endswith("odx-f"):
                dlc_element = ElementTree.parse(odx_file_name).find("FLASH")
                self._flash = NamedItemList(lambda x: x.short_name, [read_flash_from_odx(dlc_element)])
                self.finalize_init()

    def finalize_init(self):
        # Create wrapper objects
        self._diag_layers = NamedItemList(
            lambda dl: dl.short_name, chain(*(dlc.diag_layers for dlc in self.diag_layer_containers)))
        self._ecus = NamedItemList(
            lambda ecu: ecu.short_name, chain(*(dlc.ecu_variants for dlc in self.diag_layer_containers)))

        # Build id_lookup
        self._id_lookup = {}  # dict

        for dlc in self.diag_layer_containers:
            self.id_lookup.update(dlc._build_id_lookup())
            # build a dict which key is company_data_id, the value is company_data,
            # this is admin_data->company_doc_info->company_data_ref
            if dlc.company_datas is not None:
                for company_data in dlc.company_datas:
                    self.id_lookup[company_data.id] = company_data

        # self.id_lookup返回一个dict，使用update将新的键值对更新到self._id_lookup中
        for dl in self.diag_layers:
            self.id_lookup.update(dl._build_id_lookup())

        for comspec in self.comparam_specs:
            self.id_lookup[comspec.id] = comspec

        for comsubset in self.comparam_subsets:
            # odx-c: build a Dict[COMPARAM-SUBSET.ID: COMPARAM-SUBSET]
            self.id_lookup[comsubset.id] = comsubset
            # odx-cs: build a Dict[DATA-OBJECT-PROP.ID: DATA-OBJECT-PROP]
            for dop in comsubset.data_object_props:
                self.id_lookup[dop.id] = dop

            comsubset._build_id_lookup(self.id_lookup)

        for vis in self.vehicle_info_specs:
            vis._build_id_lookup(self.id_lookup)

        # build sn_lookup
        if self.comparam_specs is not None:
            for comparam_spec in self.comparam_specs:
                comparam_spec._build_sn_lookup(self.sn_lookup)

        if self.diag_layer_containers is not None:
            for diag_layer_container in self.diag_layer_containers:
                diag_layer_container.build_sn_lookup(self.sn_lookup)

        # Resolve odxlink references
        # DIAG-LAYER-CONTAINER
        for dlc in self.diag_layer_containers:
            dlc._resolve_references(self.id_lookup)

        # DIAG-LAYER
        for dl_type_name in ["ECU-SHARED-DATA", "PROTOCOL", "FUNCTIONAL-GROUP", "BASE-VARIANT", "ECU-VARIANT"]:
            for dl in self.diag_layers:
                if dl.variant_type == dl_type_name:
                    dl._resolve_references(self.id_lookup)

        # resolve odx-c COMPARAM-SUBSET-REF
        for comspec in self.comparam_specs:
            comspec._resolve_references(self.id_lookup)

        # resolve odx-cs: COMPARAM-SUBSET/COMPARAMS/COMPARAM/DATA-OBJECT-PROP-REF
        for comsubset in self.comparam_subsets:
            for comparam in comsubset.comparams:
                comparam._resolve_references(self.id_lookup)
            for com_comparam in comsubset.complex_comparams:
                com_comparam.resolve_references(self.id_lookup)

        for vis in self.vehicle_info_specs:
            vis._resolve_references(self.id_lookup)

        # for flash in self._flash:
        #     flash._resolve_references(self.id_lookup)

        # resolve snref references
        for dl in self.diag_layers:
            dl.resolve_snref_references(self.sn_lookup)


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

    # modify value
    @diag_layer_containers.setter
    def diag_layer_containers(self, value):
        self._diag_layer_containers = value

    @property
    def comparam_specs(self):
        return self._comparam_specs

    @property
    def comparam_subsets(self):
        return self._comparam_subsets

    @property
    def vehicle_info_specs(self):
        return self._vehicle_info_specs

    @property
    def flash(self):
        return self._flash
