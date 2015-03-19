from zope import schema
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.cache import render_cachekey
from plone.app.layout.navigation.root import getNavigationRootObject

from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _

class INews2Portlet(IPortletDataProvider):

    title = schema.TextLine(
        title=_(u'Title'),
        description=_(u'Portlet title'),
        required=True,)

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
    implements(INews2Portlet)
    title = _(u"News")

    def __init__(self, title=_(u"News"), count=5, state=('published', )):
        self.count = count
        self.state = state
        self.title = title

class Renderer(base.Renderer):

    _template = ViewPageTemplateFile('templates/news2.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request), name=u'plone_portal_state')
        self.portal = portal_state.portal()
        self.navigation_root_url = portal_state.navigation_root_url()
        self.navigation_root_path = portal_state.navigation_root_path()

    @property
    def title(self):
        title = getattr(self.data, 'title', None)
        if title:
            return title
        else:
            return _("Au hasard")

    @ram.cache(render_cachekey)
    def render(self):
        return xhtml_compress(self._template())

    @property
    def available(self):
        return len(self._data())

    def published_news_items(self):
        return self._data()

    def all_news_link(self):
        if 'news' in getNavigationRootObject(self.context, self.portal).objectIds():
            return '%s/actualites' % self.navigation_root_url
        else:
            return None

    @memoize
    def _data(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        path = self.navigation_root_path
        limit = self.data.count
        state = self.data.state
        return catalog(portal_type='News Item',
                       review_state=state,
                       path=path,
                       sort_on='Date',
                       sort_order='reverse',
                       sort_limit=limit)[:limit]

class AddForm(base.AddForm):
    form_fields = form.Fields(INews2Portlet)
    label = _(u"Add News Portlet")
    description = _(u"This portlet displays recent News Items.")

    def create(self, data):
        return Assignment(count=data.get('count', 5), state=data.get('state', ('published',)))

class EditForm(base.EditForm):
    form_fields = form.Fields(INews2Portlet)
    label = _(u"Edit News Portlet")
    description = _(u"This portlet displays recent News Items.")
