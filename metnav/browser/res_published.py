# -*- coding: utf-8 -*-
## Copyright (C) 2009 Ingeniweb - Alter Way Solutions - all rights reserved
## No publication or distribution without authorization.

from Globals import DevelopmentMode
from logging import getLogger

from zope.component import getMultiAdapter
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime

logger = getLogger("News View")

class res_published(BrowserView):

    def searchRecentXMLDocs(self, types=[], fullpath=False):
        
        pp_tool = getToolByName(self.context, 'portal_properties')
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.site_url = self.portal_state.portal_url()
        self.meta_url = pp_tool.metnav_properties.getProperty('COLLECTION_METADATA')
        self.resource_url = pp_tool.metnav_properties.getProperty('RESOURCE_URL')   
        mn_tool = getToolByName(self.context, 'portal_metadataNav')
        
        query = self.context.xq_recent2.__str__() % {
            'xquery_version': mn_tool.getXQueryVersion(),
			'resource_url':self.resource_url,
            'site_url': self.site_url,
            'meta_url': self.meta_url,
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
