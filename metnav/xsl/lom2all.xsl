<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:ld="http://namespaces.ens-lyon.fr/livredoc/"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:lom="http://ltsc.ieee.org/xsd/LOM"
    xmlns:lomfrens="http://pratic.ens-lyon.fr/xsd/LOMFRENS"
	version="1.0" exclude-result-prefixes="lom">
	<xsl:param name="url.server"> http://myserver/mypath </xsl:param>
	<xsl:param name="url.doc"> /url_default </xsl:param>
	<xsl:param name="url.img"> /url_default </xsl:param>
	<xsl:param name="img.width">200</xsl:param>
	<xsl:template name="metaLocation">
		<xsl:choose>
			<xsl:when test="starts-with(lom:lom/lom:technical/lom:location, 'xmldb:exist://')">
				<xsl:variable name="type">
					<xsl:value-of
						select="lom:lom/lom:educational/lom:learningResourceType/lom:value"/>
				</xsl:variable>
				<xsl:value-of select="$url.server"/>
				<xsl:choose>
					<xsl:when test="$type = 'figure'">
						<xsl:value-of select="$url.img"/>
					</xsl:when>
					<xsl:otherwise>
						<xsl:value-of select="$url.doc"/>
					</xsl:otherwise>
				</xsl:choose>
				<xsl:value-of select="@url"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="lom:lom/lom:technical/lom:location"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="lom:date">
		<xsl:variable name="date">
			<xsl:value-of select="lom:dateTime"/>
		</xsl:variable>
		<xsl:choose>
			<xsl:when test="string-length($date) = 10 or string-length($date) = 8">
				<xsl:value-of select="substring-after(substring-after($date, '-'), '/')"/>
				<xsl:text> / </xsl:text>
				<xsl:value-of select="substring-before(substring-after($date, '-'), '/')"/>
				<xsl:text> / </xsl:text>
				<xsl:value-of select="substring-before($date, '-')"/>
			</xsl:when>
			<xsl:when test="string-length($date) = 6">
				<xsl:value-of select="substring-after($date, '-')"/>
				<xsl:text> / </xsl:text>
				<xsl:value-of select="substring-before($date, '-')"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="$date"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="lom:entity">
		<xsl:choose>
			<xsl:when
				test="starts-with(normalize-space(.), 'BEGIN:VCARD') or starts-with(normalize-space(.), 'begin:vcard')">
				<xsl:call-template name="nomVCard"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="."/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template name="nomVCard">
		<xsl:variable name="email">
			<xsl:choose>
				<xsl:when test="contains(., 'EMAIL;INTERNET:')">
					<xsl:value-of
						select="normalize-space(substring-before(substring-after(.,'EMAIL;INTERNET:'), '&#xA;'))"
					/>
				</xsl:when>
				<xsl:when test="contains(.,'EMAIL;TYPE=internet:')">
					<xsl:value-of
						select="normalize-space(substring-before(substring-after(.,'EMAIL;TYPE=internet:'), '&#xA;'))"
					/>
				</xsl:when>
			</xsl:choose>
		</xsl:variable>
		<xsl:variable name="fn">
			<xsl:choose>
				<xsl:when test="contains(., 'FN:')">
					<xsl:value-of
						select="normalize-space(substring-before(substring-after(.,'FN:'), '&#xA;'))"
					/>
				</xsl:when>
				<xsl:when test="contains(., 'fn:')">
					<xsl:value-of
						select="normalize-space(substring-before(substring-after(.,'fn:'), '&#xA;'))"
					/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="normalize-space(.)"/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>
		<xsl:if test="email">
			<xsl:element name="a">
				<xsl:attribute name="href">
					<xsl:text>mailto:</xsl:text>
					<xsl:value-of select="$email"/>
				</xsl:attribute>
				<xsl:value-of select="$fn"/>
			</xsl:element>
		</xsl:if>
		<xsl:if test="not(email)">
			<xsl:value-of select="$fn"/>
		</xsl:if>
	</xsl:template>
	<xsl:template name="link">
		<xsl:element name="a">
			<xsl:attribute name="href">
				<xsl:call-template name="metaLocation"/>
			</xsl:attribute>
			<xsl:attribute name="title">
				<xsl:apply-templates select="lom:lom/lom:general/lom:description"/>
			</xsl:attribute>
			<xsl:value-of select="lom:lom/lom:general/lom:title/lom:string"/>
		</xsl:element>
	</xsl:template>
	<xsl:template name="contentIcon">
		<!--xsl:variable name="mime">
			<xsl:value-of select="lom:lom/lom:technical/lom:format"/>
		</xsl:variable-->
		<xsl:variable name="type">
			<xsl:value-of select="distinct-values(lom:lom/lomfrens:ensData/lomfrens:ensDocumentType/lomfrens:value)"/>
            <!--xsl:value-of select="string-join(distinct-values(lom:lom/lomfrens:ensData/lomfrens:ensDocumentType/lomfrens:value), ',')"/-->
		</xsl:variable>
		<xsl:choose>
			<xsl:when test="$type = 'article'">
                <img src="icones/article.png" alt="article.png" title="article" />
			</xsl:when>
			<xsl:when test="$type = 'image'">
                <img src="icones/type-image.png" alt="type-image.png" title="type-image" />
            </xsl:when>
            <xsl:when test="$type = 'son'">
                <img src="icones/son.png" alt="son.png" title="son" />
            </xsl:when>
            <xsl:when test="$type = 'exercice'">
                <img src="icones/exercice.png" alt="exercice.png" title="exercice" />
            </xsl:when>
            <xsl:when test="$type = 'simulation'">
                 <img src="icones/simulation.png" alt="simulation.png" title="simulation" />
            </xsl:when>
            <xsl:when test="$type = 'dossier'">
                 <img src="icones/dossier.png" alt="dossier.png" title="dossier" />
            </xsl:when>
            <xsl:when test="$type = 'simulation'">
                 <img src="icones/simulation.png" alt="simulation.png" title="simulation" />
            </xsl:when>
            <xsl:when test="$type = 'lienVersUnAutreSite'">
                 <img src="icones/lienversunautresite.png" alt="lienversunautresite.png" title="lienversunautresite" />
            </xsl:when>
			<xsl:otherwise>
				<img src="icones/telechargement.png" alt="telechargement.png" title="telechargement" />
			</xsl:otherwise>
				
			
			<xsl:when
				test="starts-with($mime, 'video/') or ($mime = 'application/vnd.rn-realmedia') or ($mime = 'application/smil')">
				<xsl:text>contenttype-movie</xsl:text>
			</xsl:when>
			<xsl:otherwise>
				<xsl:text>contenttype-document</xsl:text>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template name="authorsList">
		<xsl:for-each
			select="lom:lom/lom:lifeCycle/lom:contribute[lom:role/lom:value='author' or lom:role/lom:value='auteur']">
			<xsl:apply-templates select="lom:entity"/>
			<xsl:if test="not(position() = last())">
				<xsl:text>, </xsl:text>
			</xsl:if>
		</xsl:for-each>
	</xsl:template>
	<xsl:template match="lom:description">
		<xsl:value-of select="lom:string"/>
	</xsl:template>
	<xsl:template name="imageArticle">
		<xsl:choose>
			<xsl:when test="starts-with(lom:lom/lom:technical/lom:location, 'xmldb:exist://')">
				<xsl:variable name="doc_uri"
					select="concat('/', substring-after(substring-after(lom:lom/lom:technical/lom:location, '//'), '/'))"/>
				<xsl:variable name="doc" select="document($doc_uri)/ld:article"/>
				<xsl:variable name="first.image.titre" select="$doc//ld:illustration[1]/ld:titre[1]"/>
				<xsl:choose>
					<xsl:when
						test="contains($doc//ld:illustration[1]//ld:sourceDeLImage[1]/@urlDeLImage, '/thumb?width')">
						<a href="">
							<xsl:attribute name="href">
								<xsl:call-template name="metaLocation"/>
							</xsl:attribute>
							<img src="" alt="{$first.image.titre}">
								<xsl:attribute name="src">
									<xsl:text>http://planet-terre.ens-lyon.fr/planetterre/</xsl:text>
									<xsl:value-of
										select="substring-before($doc//ld:illustration[1]//ld:sourceDeLImage[1]/@urlDeLImage, '/thumb?')"/>
									<xsl:text>/thumb?width=</xsl:text>
									<xsl:value-of select="$img.width"/>
								</xsl:attribute>
							</img>
						</a>
					</xsl:when>
					<xsl:otherwise>
						<a href="">
							<xsl:attribute name="href">
								<xsl:call-template name="metaLocation"/>
							</xsl:attribute>
							<img src="" alt="{$first.image.titre}">
								<xsl:text>http://planet-terre.ens-lyon.fr/planetterre/</xsl:text>
								<xsl:attribute name="src">
									<xsl:value-of
										select="$doc//ld:illustration[1]//ld:sourceDeLImage[1]/@urlDeLImage"/>
									<xsl:text>/thumb?width=</xsl:text>
									<xsl:value-of select="$img.width"/>
								</xsl:attribute>
							</img>
						</a>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:when>
			<xsl:otherwise>
				<a href="{lom:lom/lom:technical/location}" alt="lom:lom/{lom:general/lom:title}">
					<xsl:value-of select="lom:lom/lom:general/lom:title"/>
				</a>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
</xsl:stylesheet>
