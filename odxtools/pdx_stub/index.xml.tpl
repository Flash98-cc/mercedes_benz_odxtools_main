{#- -*- mode: sgml; tab-width: 1; indent-tabs-mode: nil -*-
 #
 # SPDX-License-Identifier: MIT
 # Copyright (c) 2022 MBition GmbH
-#}
<?xml version="1.0" encoding="UTF-8"?>
<CATALOG xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" F-DTD-VERSION="ODX-2.2.0" xsi:noNamespaceSchemaLocation="odx-cc.xsd">
  <SHORT-NAME>{{ecu_name}}</SHORT-NAME>
  <ABLOCKS>
{%- for file_name, creation_date, mime_type in file_index %}
    <ABLOCK UPD="UNCHANGED">
      <SHORT-NAME>diagnostic_data</SHORT-NAME>
      <FILES>
        <FILE CREATION-DATE="{{creation_date}}" MIME-TYPE="{{mime_type}}">{{file_name}}</FILE>
      </FILES>
    </ABLOCK>
{%- endfor %}
  </ABLOCKS>
</CATALOG>
