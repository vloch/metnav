## Script (Python) "prefs_manage_metadata_nav_global_set"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=set metadatanav preds
##

from Products.CMFPlone import PloneMessageFactory as _
request=context.REQUEST
props = context.portal_properties.metnav_properties
list_var_str = ['EXIST_DA','URL_DOC', 'DB_XSL','XSL_CLASS_LIST', 'CONDITION_BASE','DEFAULT_COLLATION', 'HEADER_SUP','TEMPLATE_SEARCH','OBJET_SEMAINE','COLLECTION_METADATA', 'RESOURCE_URL',]
list_var_lines = ['OBJECTS', 'MEDIAS', 'DB_XSL_OPTS', 'XPATH_SEARCH_EXPR','COLLECTIONS', ]
list_var_int = ['LIMIT_RELATED','SCORE_CONNEXE','BATCH_LENGTH','INIT_ANNEE']
list_var_bool =['ARCHIVE_MOIS', 'HREF_BLANK']
for var in list_var_str:
    props.manage_changeProperties({var:request.form.get(var, '')})

for var in list_var_lines:
    items = [item for item in request.form.get(var, '').split('\n') if item != '']
    props.manage_changeProperties({var:items})

for var in list_var_int:
    props.manage_changeProperties({var:int(request.form.get(var, '0'))})

for var in list_var_bool:
    if request.form.get(var)=='False':
       props.manage_changeProperties({var:False})
    else:
       props.manage_changeProperties({var:True})

context.plone_utils.addPortalMessage('Modifications saved.')

return state






