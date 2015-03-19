from Products.CMFCore.utils import getToolByName

portal_url=context.portal_url()
mn_tool = getToolByName(context, 'portal_metadataNav')
collection=context.portal_metadataNav.getCollection(REQUEST=None).get('collection', '')
da = mn_tool.getDA()
words=[]

jsonData="""{
"query": "Unit",
"suggestions":
"""

query="""xquery version "1.0";
declare namespace lom="http://ltsc.ieee.org/xsd/LOM";
for $res in collection('%s')/lom:lom[lom:lifeCycle/lom:contribute[lom:role/lom:value='publisher']//lom:dateTime <= adjust-date-to-timezone(current-date(),())]
let $mots:= string-join(distinct-values($res/lom:general/lom:keyword/lom:string/text()), ', ')
order by $mots ascending empty least
return $mots
""" % collection

res = str(da.query(query)).encode('utf-8').replace('\n', ', ')
mots=res.split(', ')
for mot in mots:
   if mot not in words:
      #dicoMot="{'value':'%s', 'data':'%s'}" %(mot, mot)
      dicoMot='"%s":"%s"' %(mot, mot)
      words.append(dicoMot)    
jsonData+=str(words)+"}"
wordsArray="{"
for w in words:
    wordsArray+=w+", "

wordsArray+="}"
#return jsonData.replace('"', '\'')
#return str(words).replace('[', '{').replace(']', '}')
return wordsArray
