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
from zope.component.hooks import getSite

from Products.CMFPlone import PloneMessageFactory as _
from zope.interface import implements
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

#from metnav.browser.themes import IThemeBrowserView

logger = getLogger("MetNav Classification Portlet")

class IClassificationPortlet(IPortletDataProvider):
    """
    A portlet displaying a the top news
    """

class Assignment(base.Assignment):
    implements(IClassificationPortlet)
    title = _(u'Classification')

class Renderer(base.Renderer):

    _template = ViewPageTemplateFile('templates/classification.pt')

    def render(self):
        return self._template()

    def ifResTheme(self):
        #return IThemeBrowserView.providedBy(self.view)
        return True

    @property
    def portal_metadataNav(self):
        return getToolByName(self.context, 'portal_metadataNav')

    def update(self):
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.site_url = self.portal_state.portal_url()

    def classification(self,parts=None, obj='', output='class_list'):
        context = self.context
        
        # Si c'est la page 'par_theme' ou 'par_type_de_ressources'=> on n'utilise pas 'res_themes'
        # le reste de ces page --> on appelle 'res_themes'
        
        url_absolu = context.absolute_url()
        paths = url_absolu.split("/") 
        path = paths[-1]
        
        if path == "par_theme" or path=="par_type_de_ressource":
            chemin = url_absolu
        else :
            chemin = self.site_url     
            
        if parts is None:
            parts = '//Physique'
        elif parts == '':
            parts = '//'

        parts_xq = ""
        taxons = parts.strip().split('//')
        parents = taxons[:-1]
        actual_taxon = taxons[-1]

        parents_xq = ""
        for parent in parents:
            if parent.strip() != '':
                parents_xq += """/vdex:term[vdex:caption/vdex:langstring = "%s"]""" % parent

        params_dict = {
            'XSL': output,
            'PARTS': parents_xq,
            'XSL_PARAMS': {
                'ancestors': '//'.join(parents).strip(),
                'actual.taxon': actual_taxon,
                'object': obj,
                'site_url': chemin,
            }
        }
       
        query = context.xq_list_taxon.__str__() % self.portal_metadataNav.getQueryParams(params_dict, self.request) 
            
        if DevelopmentMode:
            logger.info(query)

        da = self.portal_metadataNav.getDA()
        if path == "par_theme":
            res = da.query(query, object_only=1)
        else :
            res = da.query(query, object_only=1)
            
        if DevelopmentMode:
            logger.info(repr(res))

        return str(res)
        #return parents


class AddForm(base.NullAddForm):
    def create(self):
        return Assignment()
