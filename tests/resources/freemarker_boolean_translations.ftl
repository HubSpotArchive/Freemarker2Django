<#--
This test file is full of boolean logic that needs to be Djangofied
-->

<#macro not>
<#if !true>y</#if>
</#macro>

<#macro truth>
<#if bool = true>y</#if>
</#macro>

<#macro length>
<#if str?length gt 0>y</#if>
</#macro>

<#macro length2>
<#if str?trim?length gt 0>y</#if>
</#macro>

<#macro has_content>
<#if str?has_content>y</#if>
</#macro>
