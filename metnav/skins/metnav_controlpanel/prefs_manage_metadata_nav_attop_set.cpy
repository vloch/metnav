from Products.CMFPlone import PloneMessageFactory as _
request=context.REQUEST
props = context.portal_properties.metnav_properties

props.manage_changeProperties({'TOP_DOCUMENT':request.form.get('TOP_DOCUMENT', '')})
props.manage_changeProperties({'TOP_DESCRIPTION':request.form.get('TOP_DESCRIPTION', '')})

context.plone_utils.addPortalMessage('Modifications saved.')
return state
