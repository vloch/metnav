# -*- coding: utf-8 -*-
## Copyright (C) 2009 Ingeniweb - Alter Way Solutions - all rights reserved
## No publication or distribution without authorization.
from Globals import DevelopmentMode
from zope.component import getMultiAdapter
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime

class res_archives(BrowserView):

    def archives(self, date_archives=''):
        context = self.context
        pp_tool = getToolByName(context, 'portal_properties')
        mn_tool = getToolByName(context, 'portal_metadataNav')
        affiche_mois= pp_tool.metnav_properties.getProperty('ARCHIVE_MOIS')
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.site_url = self.portal_state.portal_url()
        self.resource_url = pp_tool.metnav_properties.getProperty('RESOURCE_URL')
        collection = pp_tool.metnav_properties.getProperty('COLLECTION_METADATA')
            
        query = context.xq_archives.__str__() % {
            'COLLECTION':collection,
            'DATE_ARCHIVES':date_archives,
            'site_url': self.site_url,
			'resource_url':self.resource_url,
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
