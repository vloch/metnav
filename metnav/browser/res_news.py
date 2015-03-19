# -*- coding: utf-8 -*-
## Copyright (C) 2009 Ingeniweb - Alter Way Solutions - all rights reserved
## No publication or distribution without authorization.

from Globals import DevelopmentMode
from logging import getLogger

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime

logger = getLogger("News View")

class res_news(BrowserView):

    def getResults(self, date_limit='0000-00-00', nb_limit=0, start=1, output='page'):
        mn_tool = getToolByName(self.context, 'portal_metadataNav')

        news_params_dict = {'XSL':output,
                            'DATE_PUB_MIN':date_limit,
                            'XSL_PARAMS':{u'rss.title':"Nouveautés du site",
                                          u'rss.desc':'Toutes les nouveautés du site',
                                          u'rss.copyright':'Mon établissement',},
                            'NB_LIMIT':nb_limit,
                            'START':start,
                           }

        query = self.context.xq_news.__str() % mn_tool.getQueryParams(news_params_dict, self.request)

        if DevelopmentMode:
            logger.info(query)

        da = mn_tool.getDA()
        res = da.query(query, object_only=1)

        if DevelopmentMode:
            logger.info(repr(res))

        return str(res)
