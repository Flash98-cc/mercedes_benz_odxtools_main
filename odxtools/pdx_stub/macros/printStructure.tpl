{#- -*- mode: sgml; tab-width: 1; indent-tabs-mode: nil -*-
 #
 # SPDX-License-Identifier: MIT
 # Copyright (c) 2022 MBition GmbH
-#}

{%- import('macros/printParam.tpl') as pp %}

{%- macro printStructure(st) -%}
<STRUCTURE ID="{{st.id}}">
 <SHORT-NAME>{{st.short_name}}</SHORT-NAME>
{%- if st.long_name %}
 <LONG-NAME>{{st.long_name|e}}</LONG-NAME>
{%- endif %}
{%- if st.bit_length is not none %}
 <BYTE-SIZE>{{((st.bit_length + 7)/8)|int}}</BYTE-SIZE>
{%- endif %}
 <PARAMS>
{%- for param in st.parameters -%}
  {{ pp.printParam(param)|indent(2)}}
{%- endfor %}
 </PARAMS>
</STRUCTURE>
{%- endmacro -%}
