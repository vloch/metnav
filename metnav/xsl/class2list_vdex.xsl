<xsl:stylesheet xmlns:vdex="http://www.imsglobal.org/xsd/imsvdex_v1p0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:lom="http://ltsc.ieee.org/xsd/LOM" version="1.0" exclude-result-prefixes="vdex">
    <xsl:output encoding="UTF-8" indent="yes" omit-xml-declaration="yes" media-type="html"/>
    <xsl:param name="ancestors"/>
    <xsl:param name="object"/>
    <xsl:param name="site_url"/>
    <xsl:param name="view.details">1</xsl:param>
    <xsl:param name="actual.taxon"/>
    <xsl:template match="/">
        <xsl:apply-templates select="*"/>
    </xsl:template>
    <xsl:template match="vdex:vocabName">
        <h4>
            <xsl:value-of select="vdex:langstring"/>
        </h4>
    </xsl:template>
    <xsl:template match="res">
        <xsl:apply-templates select="vdex:term"/>
    </xsl:template>
    <xsl:template name="brother_taxon">
        <xsl:attribute name="class">
            <xsl:text>brother</xsl:text>
        </xsl:attribute>
        <xsl:attribute name="href">
            <xsl:value-of select="$site_url"/>
            <xsl:text>/res_themes?part=</xsl:text>
            <xsl:value-of select="$ancestors"/>
            <xsl:text>//</xsl:text>
            <xsl:value-of select="normalize-space(vdex:caption/vdex:langstring)"/>
            <xsl:text>&amp;obj=</xsl:text>
            <xsl:value-of select="$object"/>
        </xsl:attribute>
        <xsl:if test="$view.details != '1'">
            <xsl:attribute name="title">
                <xsl:for-each select="vdex:term">
                    <xsl:value-of select="normalize-space(vdex:caption/vdex:langstring)"/>
                    <xsl:if test="position() &lt; last()">
                        <xsl:text>, </xsl:text>
                    </xsl:if>
                </xsl:for-each>
            </xsl:attribute>
        </xsl:if>
        <xsl:value-of select="normalize-space(vdex:caption/vdex:langstring)"/>
    </xsl:template>
    <xsl:template match="vdex:term">
        <dd class="portletItem">
            <xsl:choose>
                <xsl:when test="normalize-space(vdex:caption/vdex:langstring) != $actual.taxon">
                    <a>
                        <xsl:call-template name="brother_taxon"/>
                    </a>
                </xsl:when>
                <xsl:otherwise>
                    <div>
                        <xsl:call-template name="brother_taxon"/>
                    </div>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:if test="normalize-space(vdex:caption/vdex:langstring) = $actual.taxon and vdex:term and $view.details = '1'">
                <span class="portletItemDetails">
                    <dl>
                        <xsl:for-each select="vdex:term">
                            <dd>
                                <a>
                                    <xsl:attribute name="href">
                                        <xsl:value-of select="$site_url"/>
                                        <xsl:text>/res_themes?part=</xsl:text>
                                        <xsl:value-of select="$ancestors"/>
                                        <xsl:text>//</xsl:text>
                                        <xsl:value-of select="normalize-space(../vdex:caption/vdex:langstring)"/>
                                        <xsl:text>//</xsl:text>
                                        <xsl:value-of select="normalize-space(vdex:caption/vdex:langstring)"/>
                                        <xsl:text>&amp;obj=</xsl:text>
                                        <xsl:value-of select="$object"/>
                                    </xsl:attribute>
                                    <xsl:attribute name="title">
                                        <xsl:for-each select="vdex:term">
                                            <xsl:value-of select="normalize-space(vdex:caption/vdex:langstring)"/>
                                            <xsl:if test="position() &lt; last()">
                                                <xsl:text>, </xsl:text>
                                            </xsl:if>
                                        </xsl:for-each>
                                    </xsl:attribute>
                                    <xsl:value-of select="normalize-space(vdex:caption/vdex:langstring)"/>
                                </a>
                            </dd>
                        </xsl:for-each>
                    </dl>
                </span>
            </xsl:if>
        </dd>
    </xsl:template>
</xsl:stylesheet>