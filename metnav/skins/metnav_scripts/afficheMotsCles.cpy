##parameters=url='', portal_url=''

from Products.CMFCore.utils import getToolByName

if url.strip() == '':
  return ''

url = url.replace('"',"'")
meta_url = getToolByName(context, 'portal_properties').metnav_properties.COLLECTION_METADATA
mn_tool = getToolByName(context, 'portal_metadataNav')

query = str(context.xq_motscles) % {'xquery_version': mn_tool.getXQueryVersion(),
                                    'url':url,
                                    'portal_url':portal_url,
                                    'meta_url':meta_url,}

try:
  result = str(context.exist.query(query, object_only=1)).replace('&#160;', ' ')
except:
  result = ""

return result
