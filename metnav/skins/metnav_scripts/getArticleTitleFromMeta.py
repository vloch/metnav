##parameters=url=''

from Products.CMFCore.utils import getToolByName

mn_tool = getToolByName(context, 'portal_metadataNav')

if url.strip() == '':
  return 'Document'

url = url.replace('"',"'")

QUERY="""xquery version "%(xquery_version)s";
declare namespace lom="http://ltsc.ieee.org/xsd/LOM";
let $titre := document("%(url)s")/lom:lom/lom:general/lom:title/lom:string[1]/text()
return
  $titre
""" % {'xquery_version': mn_tool.getXQueryVersion(),
       'url':url,}

try:
  retour = str(context.exist.query(QUERY, object_only=1)).replace('&#160;', ' ')
except:
  retour = "document"

return retour
