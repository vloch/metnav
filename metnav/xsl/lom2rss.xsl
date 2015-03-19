<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
	xmlns:lom="http://ltsc.ieee.org/xsd/LOM" 
	exclude-result-prefixes="lom"
	version="1.0" >
	
	<xsl:import href="lom2all.xsl"/>
	<xsl:output encoding="UTF-8" indent="yes" omit-xml-declaration="no" media-type="xml"/>
	
	<xsl:param name="rss.title">Site title</xsl:param>
	<xsl:param name="url.server">http://myserver/mypath</xsl:param>
	<xsl:param name="rss.desc">Site description</xsl:param>
	<xsl:param name="rss.language">fr-fr</xsl:param>
	<xsl:param name="rss.copyright">My copyright</xsl:param>
	<xsl:param name="site.editor">Me</xsl:param>
	<xsl:param name="site.webmaster">Me too !</xsl:param>
	
	<xsl:template match="/">
		<rss version="2.0">
			<channel>
				<title><xsl:value-of select="$rss.title"/></title>
				<link><xsl:value-of select="$url.server"/></link>
				<description><xsl:value-of select="$rss.desc"/></description>
				<language><xsl:value-of select="$rss.language"/></language>
				<copyright><xsl:value-of select="$rss.copyright"/></copyright> 
				<managingEditor><xsl:value-of select="$site.editor"/></managingEditor>
				<webMaster><xsl:value-of select="$site.webmaster"/></webMaster>
				<generator>Plone, eXist</generator>
				<xsl:apply-templates select="*"/>
			</channel>
		</rss>
	</xsl:template>
	
	<xsl:template match="res">
		<item>
			<title><xsl:value-of select="lom:lom/lom:general/lom:title/lom:string"/></title>
			<link><xsl:call-template name="metaLocation"/></link>
			<description><xsl:apply-templates select="lom:lom/lom:general/lom:description"/></description>
			<guid><xsl:value-of select="lom:lom/lom:technical/lom:location"/></guid>
			<pubDate><xsl:apply-templates select="lom:lom/lom:lifeCycle/lom:contribute[lom:role/lom:value='author' or lom:role/lom:value='auteur'][1]/lom:date"/></pubDate>
			<author><xsl:call-template name="authorsList"/></author>
		</item>
	</xsl:template>
</xsl:stylesheet>
