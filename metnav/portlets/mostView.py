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

class IMostViewPortlet(IPortletDataProvider):
    """
    A portlet displaying a the objects

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    portlet_title = schema.TextLine(title=_(u"Titre du portlet les plus vues"),
                            description=_(u"Saisissez le titre du portlet les plus vues"),
                            default= _(u"Les plus vues"),
                            required=True)
                            
    liens = schema.List(title=_(u"Liste des liens vers les ressources les plus vues."),
                             description=_(u"Saisissez entre  et 10 liens vers des métadonnées de ressources. Le lien doit être comme l'exemple suivant : /db/csphysique/metadata/LOM_CSP_exercice-satellite-periode-trace-au-sol.xml"),
                             min_length = 3,
                             max_length = 10,
                             required=True,
                             value_type = schema.TextLine())
    enableLeadImage = schema.Choice(
	        title = _(u"Lead Image ?"),
			description = _(u"Choisissez le mode de présentation"),
			default=_('Sans vignette'),
			values=['Sans vignette', 'Avec vignette', 'Avec Slider'],
			required = True,)

class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IMostViewPortlet)

    # TODO: Set default values for the configurable parameters here

    portlet_title = u"Type de ressources"
    liens = []

    # TODO: Add keyword parameters for configurable parameters here
    def __init__(self, portlet_title="",liens=[],enableLeadImage='Sans vignette'):
        self.portlet_title = portlet_title
        self.liens = liens
        self.enableLeadImage=enableLeadImage
        
    @property
    def title(self):
        """computed title"""
        return _(u"Portlet de choix des ressources les plus vues. ")

class Renderer(base.Renderer):
    _template = ViewPageTemplateFile('templates/mostView.pt')

    def update(self):
        pp_tool = getToolByName(self.context, 'portal_properties')
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.site_url = self.portal_state.portal_url()
        self.metadataNav = getToolByName(self.context, 'portal_metadataNav')

    def render(self):
        return self._template()
    
    def getRStitle(self, *metaURL):
        context=self.context
        mn_tool = getToolByName(self.context, 'portal_metadataNav')
        mn_props = getToolByName(context, 'portal_properties').metnav_properties        
        query = self.context.xq_lesPlusVues.__str__() % {
            'xquery_version':mn_tool.getXQueryVersion(),
            'url_meta': str(metaURL[0]),
            'site_url': self.site_url,
		    'resource_url': mn_props.getProperty('RESOURCE_URL'),
            }

        da = mn_tool.getDA()
        results = da.query(query.encode('utf-8'), object_only=1)

        liste_dico=results.getDict()
        retour = []
        for dico in liste_dico:
            retour.append(dico)
            
        if len(retour) == 0 and len(liste_dico) > 0:
                return liste_dico

        return retour
        
class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IMostViewPortlet)


    def create(self, data):
        return Assignment(**data)



class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IMostViewPortlet)
    label=_(u"Editer le portlet Les plus vues")
    description=_(u"Ce portlet affiche les ressources les plus vues.")


