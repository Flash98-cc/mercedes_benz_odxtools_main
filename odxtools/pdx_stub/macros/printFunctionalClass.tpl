
{#- -*- mode: sgml; tab-width: 1; indent-tabs-mode: nil -*-
 #
 # SPDX-License-Identifier: MIT
 # Copyright (c) 2022 MBition GmbH
-#}

{%- macro printFunctionalClass(fc) -%}
<FUNCT-CLASS ID="{{fc.id}}">
 <SHORT-NAME>{{fc.short_name}}</SHORT-NAME>
{%- if fc.long_name is string and fc.long_name.strip() %}
 <LONG-NAME>{{fc.long_name}}</LONG-NAME>
{%- endif %}
{%- if fc.description is string and fc.description.strip() %}
 <DESC>
{{fc.description}}
 </DESC>
{%- endif %}
</FUNCT-CLASS>
{%- endmacro -%}
