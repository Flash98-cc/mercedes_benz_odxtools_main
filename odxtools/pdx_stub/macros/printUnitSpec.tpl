{#- -*- mode: sgml; tab-width: 1; indent-tabs-mode: nil -*-
 #
 # SPDX-License-Identifier: MIT
 # Copyright (c) 2022 MBition GmbH
-#}

{%- import('macros/printElementID.tpl') as peid %}

{%- macro printUnitSpec(spec) -%}
<UNIT-SPEC>
 {%- if spec.unit_groups %}
 <UNIT-GROUPS>
 {%- for group in spec.unit_groups %}
  {{ printUnitGroup(group)|indent(2) }}
 {%- endfor %}
 </UNIT-GROUPS>
 {%- endif %}
 {%- if spec.units %}
 <UNITS>
 {%- for unit in spec.units %}
  {{ printUnit(unit)|indent(2) }}
 {%- endfor %}
 </UNITS>
 {%- endif %}
 {%- if spec.physical_dimensions %}
 <PHYSICAL-DIMENSIONS>
 {%- for dim in spec.physical_dimensions %}
  {{ printPhysicalDimesion(dim)|indent(2) }}
 {%- endfor %}
 </PHYSICAL-DIMENSIONS>
 {%- endif %}
</UNIT-SPEC>
{%- endmacro -%}


{%- macro printUnit(unit) -%}
<UNIT ID="{{unit.id}}"
 {%- filter odxtools_collapse_xml_attribute %}
  {%- if unit.oid %}
                OID="{{unit.oid}}"
  {%- endif %}
 {%- endfilter -%}>
 {{ peid.printElementID(unit) }}
 <DISPLAY-NAME>{{ unit.display_name }}</DISPLAY-NAME>
 {%- if unit.factor_si_to_unit is not none %}
 <FACTOR-SI-TO-UNIT>{{ unit.factor_si_to_unit }}</FACTOR-SI-TO-UNIT>
 {%- endif %}
 {%- if unit.offset_si_to_unit is not none %}
 <OFFSET-SI-TO-UNIT>{{ unit.offset_si_to_unit }}</OFFSET-SI-TO-UNIT>
 {%- endif %}
 {%- if unit.physical_dimension_ref %}
 <PHYSICAL-DIMENSION-REF ID-REF="{{ unit.physical_dimension_ref }}" />
 {%- endif %}
</UNIT>
{%- endmacro -%}

{%- macro printUnitGroup(group) -%}
<UNIT-GROUP {%- if group.oid %} OID="{{group.oid}}" {%- endif %}>
 {{ peid.printElementID(group) }}
 <CATEGORY>{{ group.category }}</CATEGORY>
 {%- if group.unit_refs %}
 <UNIT-REFS>
 {%- for ref in group.unit_refs %}
  <UNIT-REF ID-REF="{{ ref }}" />
 {%- endfor %}
 </UNIT-REFS>
 {%- endif %}
</UNIT-GROUP>
{%- endmacro -%}

{%- macro printPhysicalDimesion(dim) -%}
<PHYSICAL-DIMENSION ID="{{dim.id}}"
 {%- filter odxtools_collapse_xml_attribute %}
  {%- if dim.oid %}
                OID="{{dim.oid}}"
  {%- endif %}
 {%- endfilter -%}>
 {{ peid.printElementID(dim) }}
 {%- if dim.length_exp %}
 <LENGTH-EXP>{{ dim.length_exp }}</LENGTH-EXP>
 {%- endif %}
 {%- if dim.mass_exp %}
 <MASS-EXP>{{ dim.mass_exp }}</MASS-EXP>
 {%- endif %}
 {%- if dim.time_exp %}
 <TIME-EXP>{{ dim.time_exp }}</TIME-EXP>
 {%- endif %}
 {%- if dim.current_exp %}
 <CURRENT-EXP>{{ dim.current_exp }}</CURRENT-EXP>
 {%- endif %}
 {%- if dim.temperature_exp %}
 <TEMPERATURE-EXP>{{ dim.temperature_exp }}</TEMPERATURE-EXP>
 {%- endif %}
 {%- if dim.molar_amount_exp %}
 <MOLAR-AMOUNT-EXP>{{ dim.molar_amount_exp }}</MOLAR-AMOUNT-EXP>
 {%- endif %}
 {%- if dim.luminous_intensity_exp %}
 <LUMINOUS-INTENSITY-EXP>{{ dim.luminous_intensity_exp }}</LUMINOUS-INTENSITY-EXP>
 {%- endif %}
</PHYSICAL-DIMENSION>
{%- endmacro -%}
