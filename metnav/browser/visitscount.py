# -*- coding: utf-8 -*-
## Copyright (C) 2009 Ingeniweb - Alter Way Solutions - all rights reserved
## No publication or distribution without authorization.

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from persistent.dict import PersistentDict
from persistent.list import PersistentList
from time import time

class VisitsCount(BrowserView):
    """
    This is used to count the number of visits on the different pages of the
    site.
    Visits are stored in a persistent dict that has a persistent list for each
    page id.
    The list contains the time of visits and should be cleaned of old visits
    each time they are accessed.
    """
    def get_page_id(self):
        """
        Return an id for the given page.
        """
        return '/'.join(self.context.getPhysicalPath())

    def _number_of_days(self):
        """
        Get the number of days a visit should be kept.
        """
        mn_props = getToolByName(context, 'portal_properties')['metnav_properties']
        return mn_props.getProperty('visits_count_number_of_days')

    def _clean_visits(self, visits):
        """
        Remove visits that are more than n days old.
        """
        limit_time = time() - self._number_of_days() * 24 * 3600
        while visits[0] < limit_time:
            visits.pop()

    def add_visit(self):
        """
        Add a visit for a given page.
        """
        context = self.context
        portal = getToolByName(context, 'portal_url').getPortalObject()
        if not hasattr(portal, 'visits_count'):
            portal.visits_count = visits_count = PersistentDict()
        page_id = self.get_page_id()
        if page_id not in visits_count:
            visits = visits_count[page_id] = PersistentList()
        else:
            visits = visits_count[page_id]
            self._clean_visits(visits)
        visits_count.append(time())
