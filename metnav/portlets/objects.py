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


class IObjectsPortlet(IPortletDataProvider):
    """
    A portlet displaying a the objects

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    portlet_title = schema.TextLine(title=_(u"Titre du portlet objets"),
                            description=_(u"Saisissez le titre du portlet objets"),
                            required=True)
                            
    categories = schema.List(title=_(u"Liste des categories prises en compte"),
                             required=True,
                             value_type = schema.TextLine())

class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IObjectsPortlet)

    # TODO: Set default values for the configurable parameters here

    portlet_title = u"Type de ressources"
    categories = []

    # TODO: Add keyword parameters for configurable parameters here
    def __init__(self, portlet_title="",categories=[]):
        self.portlet_title = portlet_title
        self.categories = categories
        
    @property
    def title(self):
        """computed title"""
        return _(u"Portlet de choix des ressources : ") + self.portlet_title

class Renderer(base.Renderer):
    _template = ViewPageTemplateFile('templates/objects.pt')

    def update(self):
        pp_tool = getToolByName(self.context, 'portal_properties')
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.site_url = self.portal_state.portal_url()
        self.metadataNav = getToolByName(self.context, 'portal_metadataNav')

    def render(self):
        return self._template()

    def getPart(self):
        request = self.context.request
        parts = request.get('part')
        
        if parts is None:
            parts = '//Physique'
        elif parts == '':
            parts = '//'
            
        return parts
      

class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IObjectsPortlet)


    def create(self, data):
        return Assignment(**data)



class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IObjectsPortlet)
    label=_(u"Editer le portlet Objects")
    description=_(u"Ce portlet affiche les types de ressouces.")


