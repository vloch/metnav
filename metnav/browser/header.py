# -*- coding: utf-8 -*-
## Copyright (C) 2009 Ingeniweb - Alter Way Solutions - all rights reserved
## No publication or distribution without authorization.

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

class headerview(BrowserView):

    def get_meta_tags(self, meta_dict):
        meta_html = """<meta name="%(name)s" content="%(value)s" />"""
        list_tags = [{'xml':'result/lom/general/keyword/string','meta':'keywords','action':'join'},
                     {'xml':'result/lom/general/description/string','meta':'description','action':'first'},
                     {'xml':'result/lom/lifeCycle/contribute/entity','meta':'DC.creator','action':'first'},
                     {'xml':'result/lom/general/keyword/string','meta':'DC.subject','action':'join'},
                     {'xml':'result/lom/general/description/string','meta':'DC.description','action':'first'},
                     {'xml':'result/lom/lifeCycle/contribute/date/dateTime','meta':'DC.created','action':'first'},
                     {'xml':'result/lom/general/coverage/string','meta':'DC.coverage','action':'first'},
                    ]

        out_list = []
        for t in list_tags:
            if t['action'] == 'join':
                v = ', '.join(meta_dict.get(t['xml'],['']))
            else:
                v = meta_dict.get(t['xml'],[''])[0]
            out_list.append(meta_html % {'name':t['meta'],'value':v})

        return "\n".join(out_list)

    def isXMLdoc(self, template = None):
        portal = getToolByName(self.context, "portal_url").getParentNode()
        if template is None:
            obj = self.context
        else:
            obj = template
        try:
            return portal.portal_properties['metnav_properties'].getProperty('URL_DOC','a_totally_impossible_address') in obj.absolute_url()
        except:
            pass

        return False
