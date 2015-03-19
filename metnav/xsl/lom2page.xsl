<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
	xmlns:lom="http://ltsc.ieee.org/xsd/LOM" 
    xmlns:lomfrens="http://pratic.ens-lyon.fr/xsd/LOMFRENS"
	exclude-result-prefixes="lom"
	version="1.0" >
	
	<xsl:import href="lom2all.xsl"/>
	<xsl:output encoding="UTF-8" indent="yes" omit-xml-declaration="yes" media-type="html"/>
	
	<xsl:template match="/">
			<xsl:apply-templates select="*"/>
	</xsl:template>
	
	<xsl:template match="res">
		<dl>
			<dt>
				<span>
					<!--xsl:attribute name="class"-->
						<!--xsl:call-template name="contentIcon"/-->
						<xsl:text> visualIconPadding</xsl:text>
					<!--/xsl:attribute-->
					<xsl:call-template name="link"/>
				</span>
				<span class="discreet">
					par <xsl:call-template name="authorsList"/>,
					mis à jour le 
					<xsl:apply-templates select="lom:lom/lom:lifeCycle/lom:contribute[lom:role/lom:value='publisher'][1]/lom:date"/>
				</span>
			</dt>
			
			<dd>
				<xsl:value-of select="lom:lom/lom:general/lom:description/lom:string"/>
			</dd>
		</dl>
	</xsl:template>
</xsl:stylesheet>
