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

class res_dossierthematique(BrowserView):

    def dossierThematique(self, types=[], fullpath=False, cheminDossier=''):
        context = self.context
        pp_tool = getToolByName(self.context, 'portal_properties')
        mn_tool = getToolByName(context, 'portal_metadataNav')
        site_url = context.portal_url()
		
        resource_url = pp_tool.metnav_properties.getProperty('RESOURCE_URL')        
        meta_url = pp_tool.metnav_properties.getProperty('COLLECTION_METADATA')
        
        query = self.context.xq_dossier.__str__() % {
            'xquery_version': mn_tool.getXQueryVersion(),
            'meta_url':meta_url,
            'url_dossier':cheminDossier,
            'site_url': site_url,
			'resource_url':resource_url,
            }
        da = mn_tool.getDA()
        results = da.query(query, object_only=1)

        liste_dico=results.getDict()
        retour = []
        for dico in liste_dico:
            retour.append(dico)
            
        if len(retour) == 0 and len(liste_dico) > 0:
                return liste_dico

        return retour