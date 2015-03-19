from Products.CMFCore.utils import getToolByName
mn_tool = getToolByName(context, 'portal_metadataNav')
pp_tool = getToolByName(context, 'portal_properties')
resource_url = pp_tool.metnav_properties.getProperty('RESOURCE_URL')
collection=context.portal_metadataNav.getCollection(REQUEST=None).get('collection', '')
query ="""xquery version "%s";
declare namespace lom="http://ltsc.ieee.org/xsd/LOM";
declare namespace lomfrens="http://pratic.ens-lyon.fr/xsd/LOMFRENS";

<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
	<url>
		<loc>%s</loc>
		<lastmod>{adjust-date-to-timezone(current-date(), ())}</lastmod>
		<changefreq>daily</changefreq>
		<priority>0.8</priority>
	</url>
	{
""" % (mn_tool.getXQueryVersion(), context.portal_url())
query +="""for $meta in collection('%s')/lom:lom[lom:lifeCycle/lom:contribute[lom:role/lom:value = 'publisher']/lom:date/lom:dateTime <= adjust-date-to-timezone(current-date(), ())]""" % collection
query +="""  let $url := normalize-space($meta/%s),
                 $lastmod := $meta/lom:contribute[lom:role/lom:value='publisher']/lom:date/lom:dateTime/text()
                 order by $lastmod descending empty least
                 return
                    <url>
					    <loc>{$url}</loc>
                        <lastmod>{$lastmod}</lastmod>
                        <changefreq> yearly </changefreq>
                    </url>
         }
</urlset>""" % (resource_url)
da = mn_tool.getDA()
res = str(da.query(query))

return """<?xml version="1.0" encoding="utf-8"?>\n""" + res