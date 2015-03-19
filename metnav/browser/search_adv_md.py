# -*- coding: utf-8 -*-
## Copyright (C) 2009 Ingeniweb - Alter Way Solutions - all rights reserved
## No publication or distribution without authorization.

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime
from string import capwords
from metnav import TEMPLATE_SEARCH_SCORE

class search_adv_md(BrowserView):

    def search_adv_md(self, form={}, nb_limit=0, start=0, output='page'):
        mn_tool = getToolByName(self.context, 'portal_metadataNav')
        SEARCH_TEMPLATE = getToolByName(self.context, 'portal_properties')['metnav_properties'].getProperty('TEMPLATE_SEARCH')

        if form == {} :
            return ""

        adict = {}
        for k in form.keys():
            if form[k]:
                nk = mn_tool.getXPathFromField(k)
                if nk is not None:
                    adict[nk] = form[k] 
                

        REMOVED_CHARS = ",.;:/\\\"'&\n"
        REPLACE_CHAR = " "
        search_string = ""
        score_items = []

        for k,v in adict.items():

            search_terms = v
            # Remove all special characters and replace them by a space char
            for c in REMOVED_CHARS:
                search_terms = search_terms.replace(c, REPLACE_CHAR)

            search_terms = capwords(search_terms.lower())
            search_items = []
            for search_item in search_terms.split(REPLACE_CHAR):
                search_items.append(SEARCH_TEMPLATE % (k, search_item))
                score_items.append("count($res/%s[" % (k) + SEARCH_TEMPLATE % ('.', search_item) + "])")
            search_string += "[" + ' and '.join(search_items) + "]"

        if len(adict) == 1 and adict.has_key('.'):
            for score_item in TEMPLATE_SEARCH_SCORE:
                score_items.append((score_item['value'] % ' or '.join(search_items)) + " * %d" % score_item['weight'])

        score_string = ' + '.join(score_items)

        search_params_dict = {  'SEARCH_TERMS':search_string, 
                                'SEARCH_SCORE':score_string, 
                                'START':start,
                                'NB_LIMIT':nb_limit,
                                'XSL':output,}

        query = (str(self.context.xq_search) % mn_tool.getQueryParams(search_params_dict, self.request))

        self.context.plone_log('search', query)
        da = mn_tool.getDA()
        res = da.query(query, object_only=1)

        return str(res)

