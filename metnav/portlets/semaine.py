# -*- coding: utf-8 -*-
## Copyright (C) 2009 Ingeniweb - Alter Way Solutions - all rights reserved
## No publication or distribution without authorization.


from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFCore.utils import getToolByName
from zope.interface import implements
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class ISemainePortlet(IPortletDataProvider):
    """
    A portlet displaying a the top news
    """

class Assignment(base.Assignment):
    implements(ISemainePortlet)
    title = _(u'Semaine')

class Renderer(base.Renderer):
    _template = ViewPageTemplateFile('templates/semaine.pt')

    def render(self):
        return self._template()

    def semaine(self,output='portlet'):
        context = self.context
        mn_tool = getToolByName(context, 'portal_metadataNav')
        mn_props = getToolByName(context, 'portal_properties').metnav_properties

        params_dict = {'XSL':output,
                       'XSL_PARAMS':{'rss.title':"Semaine",
                                    'rss.desc':u'Une ressource de la semaine',
                                    'rss.copyright':u'Mon établissement',},
                       'COLLATION':'',
                       'OBJECT_TYPE':mn_props.getProperty('OBJET_SEMAINE', '[lom:educational/lom:learningResourceType = "figure"]'),
                    }

        query = (str(context.xq_semaine) % mn_tool.getQueryParams(params_dict, self.request))

        da = mn_tool.getDA()

        res = da.query(query.encode('utf-8'), object_only=1)

        return str(res)

class AddForm(base.NullAddForm):
    def create(self):
        return Assignment()
