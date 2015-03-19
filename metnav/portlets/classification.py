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

from zope import schema
from zope.formlib import form
from z3c.form.browser.multi import MultiWidget

from Products.CMFPlone import PloneMessageFactory as _
from zope.interface import implements
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

#from metnav.browser.themes import IThemeBrowserView

logger = getLogger("MetNav Classification Portlet")

class IClassificationPortlet(IPortletDataProvider):
    """
    A portlet displaying a the top news
    """
    portlet_title = schema.TextLine(title=_(u"Titre du portlet Classification"),
                            description=_(u"Saisissez le titre du portlet Classification"),
                            default=_(u"Thèmes scientifiques"),
                            required=True)
                            
    portlet_discipline = schema.TextLine(title=_(u"Discipline"),
                            description=_(u"Saisissez une discipline qui apparaît dans les balises <vocabName> de la classification et correspond au chemin disciplinaire choisi ci-dessous."),
                            default= _(u""),
                            required=True)

class Assignment(base.Assignment):
    implements(IClassificationPortlet)
    title = _(u'Thèmes scientifiques')
    portlet_discipline = _(u'')
    def __init__(self, portlet_title="", portlet_discipline=""):
        self.portlet_title = portlet_title
        self.portlet_discipline = portlet_discipline
    @property
    def title(self):
        """computed title"""
        return _(u"Thèmes scientifiques")
        
class Renderer(base.Renderer):

    _template = ViewPageTemplateFile('templates/classification.pt')

    def render(self):
        return self._template()

    def ifResTheme(self):
        #return IThemeBrowserView.providedBy(self.view)
        return True
    @property
    def title(self):
        """computed title"""
        return self.data.portlet_title
        
    @property
    def discipline(self):
        """computed title"""
        discipline = self.data.portlet_discipline
        part = "//"+discipline.encode('utf-8')
        return part

    @property
    def portal_metadataNav(self):
        return getToolByName(self.context, 'portal_metadataNav')

    @property
    def getClassificationName(self):
        return self.portal_metadataNav.getCollection(self.request).get('name', '')

    def update(self):
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.site_url = self.portal_state.portal_url()

    def classification(self,parts=None, urn='', termes='', obj='', media='', output='class_list'):
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
            #chemin = url_absolu

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
				'termes': termes,
                'object': obj,
                'media' : media,
                'site_url': chemin,
				'urn':urn, 
            }
        }

        query = context.xq_list_taxon.__str__() % self.portal_metadataNav.getQueryParams(params_dict, self.request)
        query = query

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


class AddForm(base.AddForm):

    form_fields = form.Fields(IClassificationPortlet)
    
    def create(self, data):
        return Assignment(**data)

class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IClassificationPortlet)
    label=_(u"Editer le portlet Classification")
    description=_(u"Ce portlet affiche la taxonimie disciplinaire.")
