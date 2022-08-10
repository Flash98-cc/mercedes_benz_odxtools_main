{#- -*- mode: sgml; tab-width: 1; indent-tabs-mode: nil -*-
 #
 # SPDX-License-Identifier: MIT
 # Copyright (c) 2021-2022 MBition GmbH
-#}
{%- import('macros/printVariant.tpl') as pv -%}
{%- import('macros/printAdminData.tpl') as pad -%}
{%- import('macros/printCompanyData.tpl') as pcd -%}


<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<ODX MODEL-VERSION="2.2.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="odx.xsd">
 <!-- Written by the odxtools python module, version {{odxtools_version}} -->
 <DIAG-LAYER-CONTAINER ID="{{dlc.id}}">
  <SHORT-NAME>{{dlc.short_name}}</SHORT-NAME>
{%- if dlc.long_name %}
  <LONG-NAME>{{dlc.long_name|e}}</LONG-NAME>
{%- endif %}
{%- if dlc.description %}
  <DESC>
{{dlc.description}}
  </DESC>
{%- endif %}
{%- if dlc.admin_data %}
  {{pad.printAdminData(dlc.admin_data)|indent(2)}}
{%- endif %}
{%- if dlc.company_datas %}
  <COMPANY-DATAS>
 {%- for cd in dlc.company_datas %}
   {{pcd.printCompanyData(cd)|indent(3)}}
 {%- endfor %}
  </COMPANY-DATAS>
{%- endif %}
{%- if dlc.protocols %}
  <PROTOCOLS>
 {%- for dl in dlc.protocols %}
   {{pv.printVariant(dl, "PROTOCOL")|indent(3)}}
 {%- endfor %}
  </PROTOCOLS>
{%- endif %}
{%- if dlc.functional_groups %}
  <FUNCTIONAL-GROUPS>
 {%- for dl in dlc.functional_groups %}
  {{pv.printVariant(dl, "FUNCTIONAL-GROUP")|indent(3)}}
 {%- endfor %}
  </FUNCTIONAL-GROUPS>
{%- endif %}
{%- if dlc.ecu_shared_datas %}
  <ECU-SHARED-DATAS>
 {%- for dl in dlc.ecu_shared_datas %}
  {{pv.printVariant(dl, "ECU-SHARED-DATA")|indent(3)}}
 {%- endfor %}
  </ECU-SHARED-DATAS>
{%- endif %}
{%- if dlc.base_variants %}
  <BASE-VARIANTS>
 {%- for dl in dlc.base_variants %}
  {{pv.printVariant(dl, "BASE-VARIANT")|indent(3)}}
 {%- endfor %}
  </BASE-VARIANTS>
{%- endif %}
{%- if  dlc.ecu_variants %}
  <ECU-VARIANTS>
 {%- for dl in dlc.ecu_variants %}
  {{pv.printVariant(dl, "ECU-VARIANT")|indent(3)}}
 {%- endfor %}
  </ECU-VARIANTS>
{%- endif %}
 </DIAG-LAYER-CONTAINER>
</ODX>
