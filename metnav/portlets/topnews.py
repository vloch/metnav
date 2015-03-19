# -*- coding: utf-8 -*-
## Copyright (C) 2009 Ingeniweb - Alter Way Solutions - all rights reserved
## No publication or distribution without authorization.

from Globals import DevelopmentMode
from logging import getLogger

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from plone.memoize.view import memoize
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
#from zope.component.hooks import getSite

from Products.CMFPlone import PloneMessageFactory as _
from zope.interface import implements
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

logger = getLogger("TopNews Portlet")

class ITopNewsPortlet(IPortletDataProvider):
    """
    A portlet displaying a the top news
    """

class Assignment(base.Assignment):
    implements(ITopNewsPortlet)
    title = _(u'A la une')

class Renderer(base.Renderer):
    _template = ViewPageTemplateFile('templates/topnews.pt')

    def render(self):
        return self._template()

    def update(self):
        pp_tool = getToolByName(self.context, 'portal_properties')
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.site_url = self.portal_state.portal_url()
        self.top_description = pp_tool.metnav_properties.getProperty('TOP_DESCRIPTION')
        self.top_document = pp_tool.metnav_properties.getProperty('TOP_DOCUMENT')
        self.resource_url = pp_tool.metnav_properties.getProperty('RESOURCE_URL')

    def top_news(self):
        # get the description of the document "a_la_une"
        mn_tool = getToolByName(self.context, 'portal_metadataNav')

        query = self.context.xq_alaune.__str__() % {
            'xquery_version':mn_tool.getXQueryVersion(),
            'url_meta': self.top_document.strip().strip('\n'),
            'site_url': self.site_url,
            'resource_url':self.resource_url,
        }

        if DevelopmentMode:
            logger.info(query)

        da = mn_tool.getDA()
        res = da.query(query)

        if DevelopmentMode:
            logger.info(repr(res))

        return str(res)



class AddForm(base.NullAddForm):
    def create(self):
        return Assignment()
