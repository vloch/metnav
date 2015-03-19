<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
	xmlns:lom="http://ltsc.ieee.org/xsd/LOM" 
	exclude-result-prefixes="lom"
	version="1.0" >
	
	<xsl:import href="lom2all.xsl"/>
	<xsl:output encoding="UTF-8" indent="no" omit-xml-declaration="yes" media-type="text"/>
	<xsl:strip-space elements="*" />
	
	<xsl:template match="/">
		<xsl:text>[</xsl:text><xsl:apply-templates select="*"/><xsl:text>]</xsl:text>
	</xsl:template>
	
	<xsl:template match="res">
		<xsl:text>{</xsl:text>
		<xsl:apply-templates select="lom:lom/*"/>
		<xsl:text>},</xsl:text>
	</xsl:template>
	
	<xsl:template match="lom:lom//*">
		<xsl:text>"</xsl:text>
		<xsl:value-of select="name(.)"/>
		<xsl:text>":{</xsl:text>
		<xsl:if test="normalize-space(text()) != ''">
			<xsl:text>"text()":"</xsl:text>
			<xsl:value-of select="text()"/>
			<xsl:text>",</xsl:text>
		</xsl:if>
		<xsl:if test="child::*">
			
			<xsl:apply-templates select="child::*"/>
			
		</xsl:if>
		<xsl:text>},</xsl:text>
	</xsl:template>
</xsl:stylesheet>
