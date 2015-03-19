# -*- coding: utf-8 -*-
## Copyright (C) 2009 Ingeniweb - Alter Way Solutions - all rights reserved
## No publication or distribution without authorization.
from Globals import DevelopmentMode

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from plone.memoize.view import memoize
from zope.component import getMultiAdapter
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
#from zope.app.component.hooks import getSite

from zope import schema
from zope.formlib import form
from z3c.form.browser.multi import MultiWidget

from Products.CMFPlone import PloneMessageFactory as _
from zope.interface import implements
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from logging import getLogger
from DateTime import DateTime
#from metnav.browser import getRscIcon

#logger = getLogger("News View")

class IImageSemainePortlet(IPortletDataProvider):
    """
    A portlet displaying a the picture for a week

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    portlet_title = schema.TextLine(title=_(u"Titre du portlet Image de la semaine"),
                            description=_(u"Saisissez le titre du portlet Image de la semaine."),
                            default= _(u"Image de la semaine"),
                            required=True)
                            
    display_footer = schema.Bool( title = _(u"Display the link to all Images de la semaine"),
            description = _(u"Display the link to all Images de la semaine."),
            default = True,
            required = False)


class Assignment(base.Assignment):

    implements(IImageSemainePortlet)

    def __init__(self, portlet_title=_(u"Image de la semaine"), display_footer=True):
        self.display_footer = display_footer
        self.portlet_title = portlet_title
        
    def title(self):
        return self.data.portlet_title
        
class Renderer(base.Renderer):
    _template = ViewPageTemplateFile('templates/imageSemaine.pt')

    def update(self):
        pp_tool = getToolByName(self.context, 'portal_properties')
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.site_url = self.portal_state.portal_url()
        self.metadataNav = getToolByName(self.context, 'portal_metadataNav')
        self.meta_url = pp_tool.metnav_properties.getProperty('COLLECTION_METADATA')
        self.typeObjet = pp_tool.metnav_properties.getProperty('OBJET_SEMAINE')

    def render(self):
        return self._template()
    
    @property
    def titleImageSemaine(self):
        return self.data.portlet_title
    
    @property
    def displayFooter(self):
        return self.data.display_footer
    
   
    def searchImagesSemaine(self, ullpath=False):

        context = self.context
        exist = context.exist
        meta_url = self.meta_url

        mn_tool = getToolByName(self.context, 'portal_metadataNav')
        
        query = self.context.xq_lastImageSemaine.__str__() % {
            'meta_url':meta_url,
            'site_url': self.site_url,
            'OBJECT_TYPE' : self.typeObjet,
            }
            
        da = mn_tool.getDA()
        results = da.query(query)
        
        liste_dico=results.getDict()
        retour = []
        for dico in liste_dico:
            retour.append(dico)
            
        if len(retour) == 0 and len(liste_dico) > 0:
                return liste_dico

        if DevelopmentMode:
            if str(results):
                logger.info('\nRESULTS\n' + str(results))
            else:
                logger.info('\nNO RESULT\n')

        return retour
     
        
class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IImageSemainePortlet)
    label=_(u"Ajouter le portlet Image de la Semaine")
    description=_(u"Ce portlet la dernière image de la semaine.")

    def create(self, data):
        return Assignment()

class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IImageSemainePortlet)
    label=_(u"Editer le portlet Image de la Semaine")
    description=_(u"Ce portlet affiche la dernière image de la semaine.")