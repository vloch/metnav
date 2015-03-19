# -*- coding: utf-8 -*-
## Copyright (C) 2009 Ingeniweb - Alter Way Solutions - all rights reserved
## No publication or distribution without authorization.
from Globals import DevelopmentMode
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

class IRelatedPortlet(IPortletDataProvider):
    """
    A portlet displaying The related resources
    """
    portlet_title = schema.TextLine(title=_(u"Titre du portlet Voir aussi"),
                            description=_(u"Saisissez le titre du portlet Voir aussi."),
                            default= _(u"Voir aussi"),
                            required=True)
    count = schema.Int(title=_(u"Nombre d'éléments à afficher"),
                            description=_(u"Saisissez le nombre d'éléments affichés."),
                            required=True,
                            default=5)
    enableLeadImage = schema.Choice(
	        title = _(u"Lead Image ?"),
			description = _(u"Choisissez le mode de présentation"),
			default=_('Sans vignette'),
			values=['Sans vignette', 'Avec Slider'],
			required = True,)

class Assignment(base.Assignment):
    implements(IRelatedPortlet)
#    title = _(u'Related')
    def __init__(self, portlet_title=_(u'Related'), count=5, enableLeadImage='Sans vignette'):
        self.count = count
        self.portlet_title = portlet_title
        self.enableLeadImage =enableLeadImage
    def title(self):
        return self.data.portlet_title

class Renderer(base.Renderer):
    _template = ViewPageTemplateFile('templates/related.pt')

    def render(self):
        return self._template()

    def update(self):
        pp_tool = getToolByName(self.context, 'portal_properties')
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.site_url = self.portal_state.portal_url()
        self.metadataNav = getToolByName(self.context, 'portal_metadataNav')
        self.meta_url = pp_tool.metnav_properties.getProperty('COLLECTION_METADATA')
        self.resource_url = pp_tool.metnav_properties.getProperty('RESOURCE_URL')

    @property
    def portlet_title(self):
        return self.data.portlet_tittle
    
    def recentNbr(self):
        return self.data.count
		
    def enableLeadImage(self):
        return self.data.enableLeadImage
    def metnav_properties(self):
        return getToolByName(self.context, 'portal_properties').metnav_properties

    def related(self,meta_url, start=1, nb_limit=0, output='portlet'):
        context = self.context
        mn_tool = getToolByName(context, 'portal_metadataNav')
        mn_props = getToolByName(context, 'portal_properties').metnav_properties
        collection = mn_props.getProperty('COLLECTION_METADATA')

        params_dict = {'XSL':output,
                            'XSL_PARAMS':{'rss.title':"Voir aussi",
                                          'rss.desc':u'Documents connexes',
                                          'rss.copyright':u'Mon établissement',},
                            'NB_LIMIT':nb_limit,
                            'START':start,
                            'SCORE_CONNEXE':mn_props.getProperty('SCORE_CONNEXE', 10),
                            'META_URL':meta_url,
                            'COLLATION':'',
                           }
                          

        #query = (str(context.xq_related) % mn_tool.getQueryParams(params_dict, self.request))
        query = context.xq_related.__str__() %  {
            'META_URL':meta_url,
            'SCORE_CONNEXE':mn_props.getProperty('SCORE_CONNEXE', 10),
            'COLLECTION':collection,
            'site_url': self.site_url,
            'resource_url':mn_props.getProperty('RESOURCE_URL'),
			'xquery_version': mn_tool.getXQueryVersion(),	
            }


        da = mn_tool.getDA()
        results = da.query(query.encode('utf-8'))
        
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
    form_fields = form.Fields(IRelatedPortlet)
    label=_(u"Ajouter le portlet Voir aussi")
    description=_(u"Ce portlet affiche d'autres ressources proches à la ressource affichée.")
    def create(self, data):
        return Assignment()

class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IRelatedPortlet)
    label=_(u"Editer le portlet Voir aussi")
    description=_(u"Ce portlet affiche d'autres ressources proches à la ressource affichée.")