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
#from zope.component.hooks import getSite

from zope import schema
from zope.formlib import form
from z3c.form.browser.multi import MultiWidget

from Products.CMFPlone import PloneMessageFactory as _
from zope.interface import implements
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from logging import getLogger
from DateTime import DateTime
#from metnav.browser import getRscIcon

logger = getLogger("News View")

class IRecent2Portlet(IPortletDataProvider):
    """
    A portlet displaying a the recent2

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    portlet_title = schema.TextLine(title=_(u"Titre du portlet nouveautés"),
                            description=_(u"Saisissez le titre du portlet nouveautés."),
                            default= _(u"Nouveautés du site"),
                            required=True)
    count = schema.Int(title=_(u"Nombre d'éléments à afficher"),
                            description=_(u"Saisissez le nombre d'éléments affichés."),
                            required=True,
                            default=5)

    """
    enableLeadImage = schema.Bool(
            title = _(u"Lead Image en Slider"),
            description = _(u"Enables the LiveSearch feature, which shows "
                             "live results if the browser supports "
                             "JavaScript."),
            default = True,
            required = False)
    """
    enableLeadImage = schema.Choice(
	        title = _(u"Lead Image ?"),
			description = _(u"Choisissez le mode de présentation"),
			default=_('Sans vignette'),
			values=['Sans vignette', 'Avec vignette', 'Avec Slider'],
			required = True,)

class Assignment(base.Assignment):

    implements(IRecent2Portlet)

    def __init__(self, portlet_title=_(u"Les nouveautés du site"), count=5, enableLeadImage='Sans vignette'):
        self.count = count
        self.portlet_title = portlet_title
        self.enableLeadImage =enableLeadImage
        
    def title(self):
        return self.data.portlet_title
class Renderer(base.Renderer):
    _template = ViewPageTemplateFile('templates/recent2.pt')

    def update(self):
        pp_tool = getToolByName(self.context, 'portal_properties')
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.site_url = self.portal_state.portal_url()
        self.metadataNav = getToolByName(self.context, 'portal_metadataNav')
        self.meta_url = pp_tool.metnav_properties.getProperty('COLLECTION_METADATA')
        self.resource_url = pp_tool.metnav_properties.getProperty('RESOURCE_URL')
    def render(self):
        return self._template()
    
    @property
    def title(self):
        return self.data.portlet_tittle
    
    def recentTitle(self):
        return self.data.portlet_title
    
    def recentNbr(self):
        return self.data.count
		
    def enableLeadImage(self):
        return self.data.enableLeadImage
   
    def searchRecentXMLDocs(self, types=[], fullpath=False):

        mn_tool = getToolByName(self.context, 'portal_metadataNav')
        exist = mn_tool.getDA()
        nbrNvt = self.data.count
        meta_url = self.meta_url
             
        
        query =  unicode(self.context.xq_recent2.__str__() % {
            'xquery_version':mn_tool.getXQueryVersion(),
            'meta_url':meta_url,
            'site_url': self.site_url,
			'resource_url':self.resource_url,
            })
        

        da = mn_tool.getDA()
        results = da.query(query.encode('utf-8'), object_only=1)

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

        return retour[:nbrNvt]
     
        
class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IRecent2Portlet)
    label=_(u"Ajouter le portlet Nouveautés du site")
    description=_(u"Ce portlet affiche les nouveautés du site.")

    def create(self, data):
        return Assignment()

class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IRecent2Portlet)
    label=_(u"Editer le portlet Nouveautés du site")
    description=_(u"Ce portlet affiche les nouveautés du site.")
