##parameters=encoding='utf-8'
##title=RSS
from Products.CMFCore.utils import getToolByName
MAX_ITEMS       = 10
portal_url = getToolByName(context, 'portal_url') 
portal = portal_url.getPortalObject()
sender = portal.getProperty('email_from_address')
results_exist = container.restrictedTraverse("SearchRecents").searchRecentXMLDocs(fullpath=True)[:MAX_ITEMS]

#from zLOG import LOG, INFO
s_properties=container.portal_properties.site_properties
site_title=portal.getProperty('title')
site_title= site_title.decode('utf-8')

if encoding != s_properties.default_charset:
  selected_charset = encoding
else:
  selected_charset = s_properties.default_charset

retour = """<?xml version="1.0" encoding="%s"?>
<rss xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:atom="http://www.w3.org/2005/Atom" version="2.0" >
  <channel>
    <title>%s</title>
    <link>%s</link>
    <description>Les nouveautés de %s</description>
    <language>fr-fr</language>
    <copyright>école Normale Supérieure de Lyon</copyright>
    <atom:link href="%s/nouveautes_rss" rel="self" type="application/rss+xml" />
    <generator>Plone, eXist</generator>
""" % (selected_charset, site_title, container.portal_url(), site_title, container.portal_url())

for res in results_exist:
    auteurs=context.getAuteurs(res.get('res/author', '')[0])
    retour += """
    <item>
      <title>%s</title>
      <link>%s</link>
      <description>%s</description>
      <guid>%s</guid>
       <dc:date>%s</dc:date>""" % (res.get('res/title', '')[0], res.get('res/url', '')[0], res.get('res/description', '')[0], res.get('res/url', '')[0], res.get('res/pubdate', '')[0])
    for auteur in auteurs:
        retour += """ <dc:creator>%s</dc:creator> """ % auteur
    retour += """</item>"""

container.REQUEST.RESPONSE.setHeader('Content-Type', 'text/xml')
retour = retour + """  </channel>
</rss>"""
if encoding != s_properties.default_charset:
  retour = unicode(retour).encode(selected_charset)
return retour

