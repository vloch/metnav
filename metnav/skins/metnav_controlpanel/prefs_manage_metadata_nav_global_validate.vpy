## Script (Python) "prefs_manage_metadata_nav_global_validate"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Validates prefs_manage_metadata_nav
##
from Products.CMFPlone import PloneMessageFactory as _
list_var = ['EXIST_DA','OBJECTS','COLLECTIONS', 'COLLECTION_METADATA','URL_DOC',
            'DB_XSL','DB_XSL_OPTS','XSL_CLASS_LIST',
            'CONDITION_BASE','TEMPLATE_SEARCH','XPATH_SEARCH_EXPR','OBJET_SEMAINE', 'RESOURCE_URL',]
list_var_int = ['LIMITED_RELATED','BATCH_LENGTH','SCORE_CONNEXE','INIT_ANNEE']

request=context.REQUEST
for var in list_var:
    if request.form.get(var, '') == '':
        state.setError(var, _(u'Ce champ est requis.'))

for v in list_var_int:
    try:
        int(request.form.get(v,'0'))
    except:
        state.setError(v, _(u'Cette valeur doit etre un nombre entier'))

# Validation spéciale du champ collections
trouve=False
longueur_fausse = False
for c in request.form.get('COLLECTIONS', '').split('\n'):
    if c.split('|', 4)[0] == '/':
        trouve = True
    if len(c.split('|')) != 4:
        longueur_fausse = True
if not trouve:
    state.setError('COLLECTIONS',  _(u'Le chemin / est necessaire dans ce champ.'))
if longueur_fausse:
    state.setError('COLLECTIONS',  _(u'Une des lignes de ce champ a n\'a pas le bon nombre d\'elements.'))
    


if state.getErrors():
    context.plone_utils.addPortalMessage(_(u'Please correct the indicated errors.'))
    return state.set(status='failure')
else:
    return state