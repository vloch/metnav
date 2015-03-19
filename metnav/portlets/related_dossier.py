# -*- coding: utf-8 -*-
## Copyright (C) 2009 Ingeniweb - Alter Way Solutions - all rights reserved
## No publication or distribution without authorization.


from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from plone.memoize.view import memoize
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
#from zope.component.hooks import getSite

from zope import schema
from zope.formlib import form
from z3c.form.browser.multi import MultiWidget

from Products.CMFPlone import PloneMessageFactory as _
from zope.interface import implements
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from metnav.browser.themes import IThemeBrowserView

class ISerieRelatedPortlet(IPortletDataProvider):
    """
    A portlet displaying a the dossier thematique
    """

class Assignment(base.Assignment):
    implements(ISerieRelatedPortlet)
    title = _(u"Dossier thématique")

class Renderer(base.Renderer):
    _template = ViewPageTemplateFile('templates/related_dossier.pt')

    def update(self):
        pp_tool = getToolByName(self.context, 'portal_properties')
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.site_url = self.portal_state.portal_url()
        self.metadataNav = getToolByName(self.context, 'portal_metadataNav')

    def render(self):
        return self._template()

    def relatedDossier(self, url=''):
        context = self.context
        mn_tool = getToolByName(context, 'portal_metadataNav')
        query = context.xq_dossier_related.__str__() % {'url_meta': url,
            'portal_url':self.site_url,
			'xquery_version': mn_tool.getXQueryVersion(),
		}

        #da = mn_tool.getDA()
        #results = da.query(query)

        #return str(results)
        return query

    def test(self, url=''):
        context = self.context
        mn_tool = getToolByName(context, 'portal_metadataNav')
        query = str(context.xq_dossier_related)% {'url_meta': url,
            'portal_url':self.site_url,
			'xquery_version': mn_tool.getXQueryVersion(),
		}
        da = mn_tool.getDA()
        results = da.query(query)

        return str(results)

class AddForm(base.NullAddForm):
    def create(self):
        return Assignment()