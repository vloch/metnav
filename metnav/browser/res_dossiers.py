# -*- coding: utf-8 -*-
## Copyright (C) 2009 Ingeniweb - Alter Way Solutions - all rights reserved
## No publication or distribution without authorization.

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime

class res_dossiers(BrowserView):

    def dossiers(self, url_dossier='', nb_limit=0, start=0, output='page'):
        context = self.context
        mn_tool = getToolByName(context, 'portal_metadataNav')
        pp_tool = getToolByName(context, 'portal_properties')
        resource_url = pp_tool.metnav_properties.getProperty('RESOURCE_URL')
		
        if url_dossier == '':
            url_dossier = context.absolute_url()

        news_params_dict = {'XSL':output,
                            'URL_DOSSIER':url_dossier,
                            'NB_LIMIT':nb_limit,
                            'START':start,
                            'XSL_PARAMS':{'rss.title':"Dossier",
                                          'rss.desc':'Dossier',
                                          'rss.copyright':'Mon établissement',},
							'xquery_version': mn_tool.getXQueryVersion(),
							'resource_url':resource_url,
                           }

        query = (str(context.xq_dossier) % mn_tool.getQueryParams(news_params_dict, context.REQUEST))
        da = mn_tool.getDA()
        res = da.query(query, object_only=1)

        return str(res)


