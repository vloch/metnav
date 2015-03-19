from zope import schema
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements
from zope.app.form.browser import RadioWidget 

from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider

from Acquisition import aq_inner
from DateTime.DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class ISearch2Portlet(IPortletDataProvider):
    """ A portlet displaying a (live) search box
    """

    enableLivesearch = schema.Bool(
            title = _(u"Enable LiveSearch"),
            description = _(u"Enables the LiveSearch feature, which shows "
                             "live results if the browser supports "
                             "JavaScript."),
            default = True,
            required = False)

class Assignment(base.Assignment):
    implements(ISearch2Portlet)

    def __init__(self, enableLivesearch=True):
        self.enableLivesearch=enableLivesearch

    @property
    def title(self):
        return _(u"Search")


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('templates/search2.pt')

    def __init__(self, context, request, view, manager, data):
        base.Renderer.__init__(self, context, request, view, manager, data)

        portal_state = getMultiAdapter((context, request), name=u'plone_portal_state')
        self.navigation_root_url = portal_state.navigation_root_url()

    def enable_livesearch(self):
        return self.data.enableLivesearch

    def search_form(self):
        return '%s/search_form' % self.navigation_root_url
    def search_exist_form(self):
        return '%s/search_exist_form' % self.navigation_root_url

    def search_action(self):
        return '%s/search_exist' % self.navigation_root_url


class AddForm(base.AddForm):
    form_fields = form.Fields(ISearch2Portlet)
    label = _(u"Add Search Portlet")
    description = _(u"This portlet shows a search box.")

    def create(self, data):
        return Assignment()


class EditForm(base.EditForm):
    form_fields = form.Fields(ISearch2Portlet)
    label = _(u"Edit Search Portlet")
    description = _(u"This portlet shows a search box.")
