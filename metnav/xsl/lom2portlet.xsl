<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
	xmlns:lom="http://ltsc.ieee.org/xsd/LOM" 
	exclude-result-prefixes="lom"
	version="1.0" >
	
	<xsl:import href="lom2all.xsl"/>
	<xsl:output encoding="UTF-8" indent="yes" omit-xml-declaration="yes" media-type="html"/>
	
	<xsl:template match="/">
		<xsl:apply-templates select="*"/>
	</xsl:template>
	
	<xsl:template match="res">
		<dd>
			<xsl:attribute name="class">
				<xsl:text>portletItem </xsl:text>
				<xsl:choose>
					<xsl:when test="position() mod 2 = 0">
						<xsl:text>even</xsl:text>
					</xsl:when>
					<xsl:otherwise>
						<xsl:text>odd</xsl:text>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:attribute>
			<xsl:call-template name="link" />
			<div class="portletDetails">
				<xsl:apply-templates select="lom:lom/lom:metaMetadata/lom:contribute[lom:role/lom:value='publisher' or lom:role/lom:value='publisher'][1]/lom:date" />
			</div>
		</dd>
	</xsl:template>
</xsl:stylesheet>
