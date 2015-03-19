# -*- coding: utf-8 -*-
## Copyright (C) 2009 Ingeniweb - Alter Way Solutions - all rights reserved
## No publication or distribution without authorization.


from OFS.SimpleItem import SimpleItem
from App.class_init import InitializeClass
from AccessControl import ClassSecurityInfo
from DocumentTemplate.DT_Util import html_quote
from AccessControl import Unauthorized, getSecurityManager, SpecialUsers
from ZODB.POSException import ConflictError
from AccessControl.SecurityManagement import newSecurityManager
from DateTime.DateTime import DateTime

# CMF imports
from Products.CMFCore.utils import UniqueObject, getToolByName
from Products.CMFCore.ActionProviderBase import ActionProviderBase
from Products.CMFCore.ActionInformation import ActionInformation
from Products.CMFCore.Expression import Expression

# Product imports
from metnav.config import *

from zLOG import LOG, INFO

class MetadataNavTool(UniqueObject, SimpleItem, ActionProviderBase):

    id = TOOL_ID
    meta_type = TOOL_META_TYPE
    title = TOOL_TITLE

    security = ClassSecurityInfo()
    security.declareObjectProtected('View')

    security.declareProtected('View', 'getDA')
    def getDA(self):
        """Returns the eXistDA used for the tool"""
        pprops = getToolByName(self, 'portal_properties')
        DA_id = pprops['metnav_properties'].getProperty('EXIST_DA')
        portal = getToolByName(self, "portal_url").getPortalObject()
        try:
            DA = getattr(portal, DA_id, None)
            name = DA.getDA()
        except:
            raise "eXist DA %s not found." % DA_id
        return DA

    def getXQueryVersion(self):
        """ Return the XQuery Version supported by the eXistDA Connector as a float
        """
        return self.getDA().getXQueryVersion()

    security.declareProtected('View', 'getXSLURL')
    def getXSLURL(self, output='page'):
        """Transforms a keyword in an XSL URL to use with eXist. See keywords in README.txt"""
        mn_props = getToolByName(self, "portal_properties")['metnav_properties']
        output = output.lower().strip()
        if output == 'page':
            return mn_props.getProperty('XSL_PAGE', '')
        if output == 'portlet':
            return mn_props.getProperty('XSL_PORTLET', '')
        if output == 'dict':
            return mn_props.getProperty('XSL_DICT', '')
        if output == 'count':
            return mn_props.getProperty('XSL_COUNT', '')
        if output == 'rss':
            return mn_props.getProperty('XSL_RSS', '')
        if output == 'class_list':
            return mn_props.getProperty('XSL_CLASS_LIST', '')
        if output == 'table':
            return mn_props.getProperty('XSL_TABLE', '')
        if output == 'year_list':
            return mn_props.getProperty('XSL_YEAR_LIST', '')
        raise "%s is not a valid value for an XSL output" % output



    security.declareProtected('View', 'getXSLParams')
    def getXSLParams(self, params={}):
        """Merge global XSL params and local params then transform them for transform eXist function :<param name="param-name1" value="param-value1"/>"""
        portal = getToolByName(self, "portal_url")
        pprops = getToolByName(self, "portal_properties")
        mn_props = pprops['metnav_properties']
        portal_url = portal()

        # Global parameters are computed here to access props and tools
        dict_params = {
                        'url.server':portal_url,
                        'url.doc':mn_props.getProperty('URL_DOC', ''),
                        'url.img':mn_props.getProperty('URL_IMG', ''),
                        'url.doc.hide':mn_props.getProperty('URL_DOC_HIDE', ''),
                        'rss.title':portal.getProperty('title',''),
                        'rss.desc':portal.getProperty('description', '').replace('\n', ' '),
                        'rss.language':pprops['site_properties'].getProperty('default_language',''),
                        'site.editor':portal.getProperty('email_from_address',''),
                        'site.webmaster':portal.getProperty('email_from_address',''),
                        'rss.copyright':portal.getProperty('email_from_address',''),
                        'img.width':str(mn_props.getProperty('IMG_WIDTH',200)),
                        'elements.by.line':str(mn_props.getProperty('NB_ROW_TABLE',3)),
                    }
        dict_params.update(params)

        xsl_params = ""
        for k in dict_params.keys():
            xsl_params += """<param name="%(name)s" value="%(value)s" />""" % {'name':k.replace('"', "'"), 'value':dict_params[k].replace('"', "'")}
        return ''.join(xsl_params)


    security.declareProtected('View', 'getQueryParams')
    def getQueryParams(self, local_params={}, REQUEST=None):
        """Computes queries global parameters and add local params passed in argument"""
        mn_props = getToolByName(self, "portal_properties")['metnav_properties']
        portal = getToolByName(self, "portal_url").getPortalObject()

        nb_limit  = local_params.get('NB_LIMIT', 0)
        if int(nb_limit) <= 0:
            limit = ""
        else:
            limit = ", %u" % int(nb_limit)


        header_dict = { 'HEAD_SUP':local_params.get('HEAD_SUP', mn_props.getProperty('HEAD_SUP','')),
                        'COLLATION':local_params.get('COLLATION', mn_props.getProperty('DEFAULT_COLLATION','')),
                        'xquery_version': self.getXQueryVersion(),
        }

        tail_dict = {'XSL': self.getXSLURL(output=local_params.get('XSL', '')),
                     'XSL_PARAMS': self.getXSLParams(params=local_params.get('XSL_PARAMS', {})),
                     'NB_LIMIT': limit,
                     'START': int(local_params.get('START',0))+1,}

        dict_collect = self.getCollection(REQUEST)
        base_dict = {'COLLECTION': dict_collect['collection'],
                        'CONDITION_BASE':mn_props.getProperty('CONDITION_BASE', ''),
                        'HEADER':str(portal.xq_header) % header_dict,
                        'TAIL':str(portal.xq_tail) % tail_dict,
                        'CONDITION_SUP':local_params.get('CONDITION_SUP',''),
                        'CLASSIFICATION_NAME':local_params.get('CLASSIFICATION_NAME', dict_collect['name']),
                        'CLASSIFICATION_URI':local_params.get('CLASSIFICATION_URI', dict_collect['classif']),
                        'XSL_PARAMS': self.getXSLParams(params=local_params.get('XSL_PARAMS', {})),
                        'xquery_version': self.getXQueryVersion(),
                        }


        base_dict.update(local_params)
        return base_dict

    def getXPathFromField(self, field):
        """Returns a xpath expression if field is known"""
        mn_props = getToolByName(self, "portal_properties")['metnav_properties']

        for i in mn_props.XPATH_SEARCH_EXPR:
            k,v = i.split('=', 1)
            if field == k:
                return v
        return None

    def getDBXSLOpts(self, local_params={}):
        """Returns a dict containing options for the docbook xsl"""
        mn_props = getToolByName(self, "portal_properties")['metnav_properties']
        new_param = {}
        for l in mn_props.getProperty('DB_XSL_OPTS', {}):
            k,v = l.split('=',1)
            new_param[k.strip()] = v.strip().replace('\n', ' ')
        new_param.update(local_params)
        return new_param

    def getObjectsDict(self, key='lom'):
        """Returns a dict containing objects and their human representation. key can be 'lom' (dict k is the lom name) or 'human' (the dict key is the human readable name)"""
        mn_props = getToolByName(self, "portal_properties")['metnav_properties']
        new_dict = {}
        for l in mn_props.getProperty('OBJECTS', {}):
            if key == 'lom':
                v,k = l.split('=',1)
            else:
                k,v = l.split('=',1)
            new_dict[k] = v
        return new_dict

    def getMetadataDict(self, url=None):
        """Returns a dict representing a metadata"""
        if url is None:
            return {}

        sgdxq = """xquery version "%s";
        let $doc := document("%s")
        return $doc
        """ % (self.getXQueryVersion(), url)
        try:
            exist = self.getDA()
            res = exist.query(sgdxq, object_only=1)
            return res.getMergedDict(xmled=False)
        except:
            return {}




    security.declareProtected('View', 'getCollectionsDict')
    def getCollectionsDict(self,):
        """Get a dict from the list configured in COLLECTIONS"""
        mn_props = getToolByName(self, "portal_properties")['metnav_properties']
        COLLECTIONS = mn_props.getProperty('COLLECTIONS',  [])
        dict = {}
        for c in COLLECTIONS:
            path, name, xml, collection = c.strip().split('|',  4)
            dict[path] = {'name':name,  'classif':xml, 'collection':collection, }
        return dict

    security.declareProtected('View', 'getCollection')
    def getCollection(self, REQUEST=None):
        """Returns the collection to use in eXist in regards of the REQUEST.
        If REQUEST is None, then the default collection (path is /) is used."""

        collections = self.getCollectionsDict()
        if REQUEST is None:
            return collections.get('/',  None)

        for c in collections.keys():
            if c in REQUEST.PATH_INFO and c != '/':
                return collections.get(c, None)

        return collections.get('/',  None)

InitializeClass(MetadataNavTool)
