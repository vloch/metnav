<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
	xmlns:lom="http://ltsc.ieee.org/xsd/LOM" 
	exclude-result-prefixes="lom"
	version="1.0" >
	
	<xsl:output encoding="UTF-8" indent="yes" omit-xml-declaration="yes" media-type="xml"/>
	
	<xsl:template match="/">
		<xsl:value-of select="count(results/res)"/>
	</xsl:template>
	
	
</xsl:stylesheet>
