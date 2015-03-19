# -*- coding: utf-8 -*-
## Copyright (C) 2009 Ingeniweb - Alter Way Solutions - all rights reserved
## No publication or distribution without authorization.

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from zope import schema
from zope.formlib import form

from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
from zope.interface import implements
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class IHasardPortlet(IPortletDataProvider):
    """
    A portlet displaying a the top news
    """
    title = schema.TextLine(
        title=_(u'Title'),
        description=_(u'Portlet title'),
        required=True,)

class Assignment(base.Assignment):
    implements(IHasardPortlet)
    title = _(u'Au hasard')

class Renderer(base.Renderer):
    _template = ViewPageTemplateFile('templates/hasard.pt')

    @property
    def title(self):
        title = getattr(self.data, 'title', None)
        if title:
            return title
        else:
            return _("Au hasard")

    def render(self):
        return self._template()

    def hasard(self,output='portlet'):
        context = self.context
        mn_tool = getToolByName(context, 'portal_metadataNav')
        pp_tool = getToolByName(context, 'portal_properties')
        self.portal_state = getMultiAdapter((context, self.request),
                                            name=u'plone_portal_state')
        self.site_url = self.portal_state.portal_url()
        self.resource_url = pp_tool.metnav_properties.getProperty('RESOURCE_URL')

        params_dict = {'XSL':output,
                        'XSL_PARAMS':{'rss.title':u"Hasard",
                                    'rss.desc':u'Une ressource du site au hasard',
                                    'rss.copyright':u'Mon établissement',},
                        'COLLATION':'',
                        'site_url': self.site_url,
                        'resource_url':self.resource_url,
                    }

        query = unicode((str(context.xq_hasard) % mn_tool.getQueryParams(params_dict, self.request)))

        da = mn_tool.getDA()

        res = da.query(query.encode('utf-8'), object_only=1)

        return str(res)

class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IHasardPortlet)

    def create(self, data):
        return Assignment(**data)

class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IHasardPortlet)
    label=_(u"Editer le portlet « Au hasard »")
    description=_(u"Ce portlet affiche une ressource au hasard.")
