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


class IObjectsMediasPortlet(IPortletDataProvider):
    """
    A portlet displaying a the objects

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    portlet_title = schema.TextLine(title=_(u"Titre du portlet objets médias"),
                            description=_(u"Saisissez le titre du portlet objets médias"),
                            required=True)
    portlet_discipline = schema.TextLine(title=_(u"Discipline"),
                            description=_(u"Saisissez le discipline qui apparaît dans les balises <vocabName> de la classification"),
                            default= _(u"Physique"),
                            required=True)
                            
class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IObjectsMediasPortlet)

    # TODO: Set default values for the configurable parameters here

    portlet_title = _(u"Types médias")
    portlet_discipline = _(u"")

    # TODO: Add keyword parameters for configurable parameters here
    def __init__(self, portlet_title="", portlet_discipline=""):
        self.portlet_title = portlet_title
        self.portlet_discipline = portlet_discipline
    
    @property
    def title(self):
        """computed title"""
        return self.data.portlet_title
    
    @property
    def discipline(self):
        """computed discipline"""
        return self.data.portlet_discipline


class Renderer(base.Renderer):
    _template = ViewPageTemplateFile('templates/objectsMedias.pt')

    def update(self):
        pp_tool = getToolByName(self.context, 'portal_properties')
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.site_url = self.portal_state.portal_url()
        self.metadataNav = getToolByName(self.context, 'portal_metadataNav')
        self.objets_medias = pp_tool.metnav_properties.getProperty('MEDIAS')
        
    def render(self):
        return self._template()

    def getPart(self):
        request = self.context.request
        parts = request.get('part')
        
        if parts is None:
            parts = '//'+self.data.portlet_discipline
        elif parts == '':
            parts = '//'
            
        return parts
    
    def getObj(self):
        request = self.context.request
        obj = request.get('obj')
        if obj is None:
            obj = ''
           
        return obj
    
    def objetsMedias(self):
        context = self.context
        
        mn_tool = getToolByName(context, 'portal_metadataNav')
        mn_props = getToolByName(context, 'portal_properties').metnav_properties
        objets_medias = mn_props.getProperty('MEDIAS')
        return objets_medias
        
class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IObjectsMediasPortlet)


    def create(self, data):
        return Assignment(**data)

class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IObjectsMediasPortlet)
    label=_(u"Editer le portlet Objects médias")
    description=_(u"Ce portlet affiche les types médias des ressources.")