from zope import schema
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.cache import render_cachekey
from plone.app.layout.navigation.root import getNavigationRootObject

from Acquisition import aq_inner
from DateTime.DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class IEvents2Portlet(IPortletDataProvider):

    count = schema.Int(title=_(u'Number of items to display'),
                       description=_(u'How many items to list.'),
                       required=True,
                       default=5)

    state = schema.Tuple(title=_(u"Workflow state"),
                         description=_(u"Items in which workflow state to show."),
                         default=('published', ),
                         required=True,
                         value_type=schema.Choice(
                             vocabulary="plone.app.vocabularies.WorkflowStates")
                         )

class Assignment(base.Assignment):
    implements(IEvents2Portlet)

    def __init__(self, count=5, state=('published', )):
        self.count = count
        self.state = state

    @property
    def title(self):
        return _(u"Events")

class Renderer(base.Renderer):

    _template = ViewPageTemplateFile('templates/events2.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        self.navigation_root_url = portal_state.navigation_root_url()
        self.portal = portal_state.portal()
        self.navigation_root_path = portal_state.navigation_root_path()
        self.navigation_root_object = getNavigationRootObject(self.context, self.portal)
        self.have_events_folder = 'events' in self.navigation_root_object.objectIds()
        self.have_evenements_folder = 'actualites/evenements' in self.navigation_root_object.objectIds()


    @ram.cache(render_cachekey)
    def render(self):
        return xhtml_compress(self._template())

    @property
    def available(self):
        return len(self._data())

    def published_events(self):
        return self._data()

    def all_events_link(self):
        if self.have_events_folder:
            return '%s/actualites/evenements' % self.navigation_root_url
        else:
            return '%s/events_listing' % self.navigation_root_url

    @memoize
    def prev_events_link(self):
        # take care dont use self.portal here since support
        # of INavigationRoot features likely will breake #9246 #9668
        return '%s/actualites/evenements/previous' % self.navigation_root_url
        #if (self.have_evenements_folder and
        #    'previous' in self.navigation_root_object['actualites']['evenements'].objectIds()):
         #   return '%s/actualites/evenements/previous' % self.navigation_root_url
        #else:
        #    return None

    @memoize
    def _data(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        limit = self.data.count
        state = self.data.state
        path = self.navigation_root_path
        return catalog(portal_type='Event',
                       review_state=state,
                       end={'query': DateTime(),
                            'range': 'min'},
                       path=path,
                       sort_on='start',
                       sort_limit=limit)[:limit]

class AddForm(base.AddForm):
    form_fields = form.Fields(IEvents2Portlet)
    label = _(u"Add Events Portlet")
    description = _(u"This portlet lists upcoming Events.")

    def create(self, data):
        return Assignment(count=data.get('count', 5), state=data.get('state', ('published',)))

class EditForm(base.EditForm):
    form_fields = form.Fields(IEvents2Portlet)
    label = _(u"Edit Events Portlet")
    description = _(u"This portlet lists upcoming Events.")
