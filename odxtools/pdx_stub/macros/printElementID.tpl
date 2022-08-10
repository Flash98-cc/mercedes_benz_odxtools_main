{#- -*- mode: sgml; tab-width: 1; indent-tabs-mode: nil -*-
 #
 # SPDX-License-Identifier: MIT
 # Copyright (c) 2022 MBition GmbH
-#}

{%- macro printElementID(element) -%}
<SHORT-NAME>{{ element.short_name }}</SHORT-NAME>
{%- if element.long_name is string and element.long_name.strip() %}
<LONG-NAME>{{ element.long_name|e }}</LONG-NAME>
{%- endif %}
{%- if element.description is string and element.description.strip() %}
<DESC>
{{ element.description }}
</DESC>
{%- endif %}
{%- endmacro -%}
