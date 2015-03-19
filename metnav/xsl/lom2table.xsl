<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:ld="http://namespaces.ens-lyon.fr/livredoc/"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:date="http://exslt.org/dates-and-times"
	xmlns:lom="http://ltsc.ieee.org/xsd/LOM" exclude-result-prefixes="lom" version="1.0">
	<xsl:import href="lom2all.xsl"/>
	<xsl:output encoding="UTF-8" indent="yes" omit-xml-declaration="yes" media-type="html"/>
	<xsl:param name="elements.by.line">4</xsl:param>
	<xsl:template match="/">
		<table align="center">
			<xsl:apply-templates select="results"/>
		</table>
	</xsl:template>
	<xsl:template match="results">
		<xsl:for-each select="res">
			<xsl:if test="(position() mod $elements.by.line) = 1">
				<xsl:variable name="RowItems"
					select="following-sibling::node()[position() &lt; number($elements.by.line)]"/>
				<tr>
					<!-- First Column -->
					<td>
						<!-- Add rowspan="$elements.by.line" if there are no other items in this row -->
						<xsl:if test="not(count($RowItems))">
							<xsl:attribute name="colspan">
								<xsl:value-of select="$elements.by.line"/>
							</xsl:attribute>
						</xsl:if>
						<!-- Insert formatted item data -->
						<xsl:apply-templates select="."/>
					</td>

					<!-- Create other columns in current row -->
					<xsl:for-each
						select="following-sibling::node()[position() &lt; number($elements.by.line)]">
						<td>
							<!-- If current node is last of current row add colspan=".." attribute -->
							<xsl:if
								test="count(following-sibling::node()[position() &lt; number($elements.by.line)]) = 0 and not(position() = number($elements.by.line)-1)">
								<xsl:attribute name="colspan">
									<xsl:value-of select="number($elements.by.line) - position()"/>
								</xsl:attribute>
							</xsl:if>

							<!-- Insert formatted item data -->
							<xsl:apply-templates select="."/>
						</td>
					</xsl:for-each>
				</tr>
			</xsl:if>
		</xsl:for-each>
	</xsl:template>
	
	<xsl:template match="res">
		<table align="center">
			<tr>
				<td class="objsem-date"> Semaine <xsl:value-of
						select="date:week-in-year(lom:lom/lom:metaMetadata/lom:contribute[lom:role='creator' or lom:role='createur'][1]/lom:date)"
					/> (<xsl:apply-templates
						select="lom:lom/lom:metaMetadata/lom:contribute[lom:role='creator' or lom:role='createur'][1]/lom:date"
					/>) </td>
			</tr>
			<tr>
				<td class="objsem-titre">
					<xsl:value-of select="lom:lom/lom:general/lom:title/lom:string"/>
				</td>
			</tr>
			<tr>
				<td class="objsem-img"><xsl:call-template name="imageArticle" /> </td>
			</tr>
		</table>
	</xsl:template>
</xsl:stylesheet>
