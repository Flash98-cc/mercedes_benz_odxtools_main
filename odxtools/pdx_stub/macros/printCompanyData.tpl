{#- -*- mode: sgml; tab-width: 1; indent-tabs-mode: nil -*-
 #
 # SPDX-License-Identifier: MIT
 # Copyright (c) 2022 MBition GmbH
-#}

{%- macro printCompanyData(company_data) -%}
<COMPANY-DATA ID="{{company_data.id}}">
 <SHORT-NAME>{{company_data.short_name|e}}</SHORT-NAME>
 {%- if company_data.long_name is not none %}
 <LONG-NAME>{{company_data.long_name|e}}</LONG-NAME>
 {%- endif %}
 {%- if company_data.description is not none %}
 <DESC>
{{company_data.description}}
 </DESC>
 {%- endif %}
 {%- if company_data.roles is not none %}
 <ROLES>
  {%- for role in company_data.roles %}
  <ROLE>{{role|e}}</ROLE>
  {%- endfor %}
 </ROLES>
 {%- endif %}
 {%- if company_data.team_members is not none %}
 <TEAM-MEMBERS>
  {%- for team_member in company_data.team_members %}
  <TEAM-MEMBER ID="{{team_member.id}}">
   <SHORT-NAME>{{team_member.short_name|e}}</SHORT-NAME>
   {%- if company_data.long_name is not none %}
   <LONG-NAME>{{team_member.long_name|e}}</LONG-NAME>
   {%- endif %}
   {%- if company_data.description is not none %}
   <DESC>
{{team_member.description}}
   </DESC>
   {%- endif %}
   {%- if team_member.roles is not none %}
   <ROLES>
    {%- for role in team_member.roles %}
    <ROLE>{{role|e}}</ROLE>
    {%- endfor %}
   </ROLES>
   {%- endif %}
   {%- if team_member.department is not none %}
   <DEPARTMENT>{{team_member.department|e}}</DEPARTMENT>
   {%- endif %}
   {%- if team_member.address is not none %}
   <ADDRESS>{{team_member.address|e}}</ADDRESS>
   {%- endif %}
   {%- if team_member.zip is not none %}
   <ZIP>{{team_member.zip|e}}</ZIP>
   {%- endif %}
   {%- if team_member.city is not none %}
   <CITY>{{team_member.city|e}}</CITY>
   {%- endif %}
   {%- if team_member.phone is not none %}
   <PHONE>{{team_member.phone|e}}</PHONE>
   {%- endif %}
   {%- if team_member.fax is not none %}
   <FAX>{{team_member.fax|e}}</FAX>
   {%- endif %}
   {%- if team_member.email is not none %}
   <EMAIL>{{team_member.email|e}}</EMAIL>
   {%- endif %}
  </TEAM-MEMBER>
  {%- endfor %}
 </TEAM-MEMBERS>
 {%- endif %}
 {%- if company_data.company_specific_info is not none %}
 <COMPANY-SPECIFIC-INFO>
  <RELATED-DOCS>
  {%- for rd in company_data.company_specific_info.related_docs %}
   <RELATED-DOC>
    {%- if rd.xdoc  is not none %}
    <XDOC>
     <SHORT-NAME>{{rd.xdoc.short_name|e}}</SHORT-NAME>
     {%- if rd.xdoc.long_name is not none %}
     <LONG-NAME>{{rd.xdoc.long_name|e}}</LONG-NAME>
     {%- endif %}
     {%- if rd.xdoc.description is not none %}
     <DESC>
{{rd.xdoc.description}}
     </DESC>
     {%- endif %}
     {%- if rd.xdoc.number is not none %}
     <NUMBER>{{rd.xdoc.number|e}}</NUMBER>
     {%- endif %}
     {%- if rd.xdoc.state is not none %}
     <STATE>{{rd.xdoc.state|e}}</STATE>
     {%- endif %}
     {%- if rd.xdoc.date is not none %}
     <DATE>{{rd.xdoc.date|e}}</DATE>
     {%- endif %}
     {%- if rd.xdoc.publisher is not none %}
     <PUBLISHER>{{rd.xdoc.publisher|e}}</PUBLISHER>
     {%- endif %}
     {%- if rd.xdoc.url is not none %}
     <URL>{{rd.xdoc.url|e}}</URL>
     {%- endif %}
     {%- if rd.xdoc.position is not none %}
     <POSITION>{{rd.xdoc.position|e}}</POSITION>
     {%- endif %}
    </XDOC>
    {%- endif %}
    {%- if rd.description is not none %}
    <DESC>
{{rd.description}}
    </DESC>
    {%- endif %}
   </RELATED-DOC>
  {%- endfor %}
  </RELATED-DOCS>
 </COMPANY-SPECIFIC-INFO>
 {%- endif %}
</COMPANY-DATA>
{%- endmacro -%}
