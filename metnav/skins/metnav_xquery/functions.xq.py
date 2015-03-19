from Products.CMFCore.utils  import getToolByName


libQuery = context.xq_functions
siteUrl = context.portal_url()
ptool = getToolByName(context, 'portal_url')
mnprop = getToolByName(context, 'portal_properties').metnav_properties
mntool = getToolByName(context, 'portal_metadataNav')

portalPath  = ptool.getPortalPath()
portalUrl   = ptool()

serverName = mntool.getDA().server

url_doc     = portalUrl + mnprop.getProperty('URL_DOC')       #portalUrl + "/XML"
url_doc_pro = portalUrl + mnprop.getProperty('URL_DOC_HIDE')  #"/acces_pro/voir_xml?url="
url_img     = portalUrl + mnprop.getProperty('URL_IMG')       #"/objets/img_sem/XML"
server_uri  = "xmldb:exist://" + serverName

query = str(libQuery) % {'SERVER_URI'   : server_uri,
                    'URL_DOC_HIDE' : url_doc_pro,
                    'URL_IMG'      : url_img,
                    'URL_DOC'      : url_doc,
                    'site_url'      : siteUrl,
                   }

return query