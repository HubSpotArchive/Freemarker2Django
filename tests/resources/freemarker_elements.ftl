<#--
This test file is full of basic elements we'll need to be able to convert.

-->

<#macro bold>
<b><#nested></b>
</#macro>

<#macro bold2>
<b><#nested /></b>
</#macro>

<#macro condition>
<#if true>TRUTH</#if>
</#macro>

<#!-- lol -->
<#macro recursion>
<@recursion />
</#macro>

<#macro nesting>
<@nesting>woa</@nesting>
</#macro>

<#macro withArgs x>
<@withArgs 1 />
</#macro>

<#macro varArgs x>
<@withArgs "${x}" />
</#macro>

<#macro manyStrings x y>
<@withArgs "${x} ${y}" />
</#macro>
