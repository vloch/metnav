# -*- coding: utf-8 -*-
## Copyright (C) 2009 Ingeniweb - Alter Way Solutions - all rights reserved
## No publication or distribution without authorization.

from Globals import DevelopmentMode
from logging import getLogger

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from zope.interface import implements
from zope.interface import Interface

logger = getLogger('Themes browser')

class IThemeBrowserView(Interface):
    """ marker interface """


class Themes(BrowserView):

    implements(IThemeBrowserView)

    def themes(self, parts='', object_type='', sort_order='$res/lom:lifeCycle/lom:contribute[1]/lom:date/lom:dateTime/text() descending', nb_limit=0, start=0, output='page'):
        context = self.context
        mn_tool = getToolByName(context, 'portal_metadataNav')

        if parts in ('','//') and object_type == '':
            return ''

        taxons = parts.strip().split('//')
        if taxons == [] and object_type.strip() == '':
            return ""

        parts_xq = ""
        for taxon in taxons:
            if taxon.strip() != '':
                parts_xq += """[contains(lom:taxon/lom:entry/lom:string/text(), "%s")]""" % taxon


        if object_type == '':
            objects = ''
        elif object_type =='texte':
            objects = """[contains(lomfrens:ensData/lomfrens:ensDocumentType, "article") or contains(lomfrens:ensData/lomfrens:ensDocumentType, "%s")]""" % object_type
            #objects = """[contains(lomfrens:ensData/lomfrens:ensDocumentType, "%s")]""" % object_type
        else:
            objects = """[contains(lomfrens:ensData/lomfrens:ensDocumentType, "%s")]""" % object_type


        # context.template.__str__() is waiting for unicode or ascii data
        # Query returns UTF-8 strings then you must decode them
        params_dict = {
            'XSL':output,
            'XSL_PARAMS': {
                'rss.title': u"Ressources par thème",
                'rss.desc': u'Ressources du site classées par thèmes',
                'rss.copyright': u'Mon établissement',
                },
            'NB_LIMIT':nb_limit,
            'START':start,
            'PARTS': parts_xq.decode('utf-8'),
            'OBJECTS': objects.decode('utf-8'),
            'TRI':sort_order,
        }

        query = context.xq_classification.__str__() % mn_tool.getQueryParams(params_dict, context.REQUEST)
        
        if DevelopmentMode:
            logger.info('\nREQUEST\n' + query)

        da = mn_tool.getDA()
        # ExistDA is waiting for UTF-8
        res = da.query(query.encode('utf-8'), object_only=1)

        if DevelopmentMode:
            if str(res):
                logger.info('\nRESULTS\n' + str(res))
            else:
                logger.info('\nNO RESULT\n')

        return str(res)
