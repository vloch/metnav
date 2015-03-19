# -*- coding: utf-8 -*-
## Copyright (C) 2009 Ingeniweb - Alter Way Solutions - all rights reserved
## No publication or distribution without authorization.

from Globals import DevelopmentMode
from logging import getLogger

from StringIO import StringIO
from string import capwords

import ho.pisa as pisa
from xmlrpclib import Fault

from DateTime import DateTime
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
try:
    from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
except ImportError:
    from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

_HTML_HEADER = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n"""

logger = getLogger('Metnav XML browser')
class HTML(BrowserView):

    def load_article_html(self, url, template='ressource'):
        #path="/var/data/precalcul/csp/"+url
        path="/opt/python-envs/precalcul/csp/"+url
        html_file=open(path, 'r')
        html=html_file.read()
        return html
class XML(BrowserView):

    def get_article_html(self, url):
        context = self.context
        traverse_subpath = self.request['traverse_subpath']
        mn_tool = getToolByName(context, 'portal_metadataNav')
        mn_props = getToolByName(context, 'portal_properties')['metnav_properties']
        collection = mn_props.getProperty('COLLECTION_METADATA')
        urlMetadata = collection+url

        #baseInternal = self.request['PATH_TRANSLATED']
        baseInternal = self.request['ACTUAL_URL']
        # ADD DOCBOOK OPTS IN XSL_PARAMS
        params_dict = {
            'XSL_PARAMS_DB': mn_tool.getXSLParams(
                mn_tool.getDBXSLOpts({
                    "base.internal": baseInternal,
                    "exist:stop-on-error": "0",
					## breaks '#name' links
                    #"html.base": context.portal_url(),
                })),
            'XSL': 'page',
            'DOC_URL': urlMetadata,
            'DB_XSL': mn_props.getProperty('DB_XSL'),
			'xquery_version': mn_tool.getXQueryVersion(),
        }

        query = (str(context.xq_XML) % mn_tool.getQueryParams(params_dict,
                                                              self.request))

        if DevelopmentMode:
            logger.info('\n\nURL\n' + url)
            logger.info('\n\nBASE\n' + context.portal_url() + \
                        mn_props.getProperty('URL_DOC') + \
                        '/' + '/'.join(traverse_subpath))
            logger.info('\n\nREQUEST\n' + query)

        da = mn_tool.getDA()
        res = str(da.query(query, object_only=1))

        if DevelopmentMode:
            if res:
                logger.info('\n\nRESULTS\n' + str(res))
            else:
                logger.info('\n\nNO RESULT\n')

        if res.startswith('<div'):
            return res

        else:
            ## we need to remove unwanted html tags (html, head, body)
            return '\n'.join(str(res).split('\n')[6:-4])

class XMLdb(BrowserView):

    def get_directArticle_html(self, url):
        context = self.context
        traverse_subpath = self.request['traverse_subpath']

        mn_tool = getToolByName(context, 'portal_metadataNav')
        mn_props = getToolByName(context, 'portal_properties')['metnav_properties']

        # ADD DOCBOOK OPTS IN XSL_PARAMS
        params_dict = {
            'XSL_PARAMS_DB': mn_tool.getXSLParams(
                mn_tool.getDBXSLOpts({
                    "base.internal": context.portal_url() + \
                                     '/prepublication' + \
                                     '/' + '/'.join(traverse_subpath),
                    ## breaks '#name' links
                    #"html.base": context.portal_url(),
                })),
            'XSL': 'page',
            'DOC_URL': url,
            'DB_XSL': mn_props.getProperty('DB_XSL'),
        }

        query = (str(context.xq_XMLdb) % mn_tool.getQueryParams(params_dict,
                                                              self.request))

        if DevelopmentMode:
            logger.info('\nREQUEST\n' + query)

        da = mn_tool.getDA()

        try:
            res = da.query(query, object_only=1)
        except Fault, error:
            return error

        if DevelopmentMode:
            if str(res):
                logger.info('\nRESULTS\n' + str(res))
            else:
                logger.info('\nNO RESULT\n')

        return str(res)
        
class XMLld(BrowserView):

    def get_directArticle_html(self, url):
        context = self.context
        traverse_subpath = self.request['traverse_subpath']

        mn_tool = getToolByName(context, 'portal_metadataNav')
        mn_props = getToolByName(context, 'portal_properties')['metnav_properties']

        # ADD DOCBOOK OPTS IN XSL_PARAMS
        params_dict = {
            'XSL_PARAMS_DB': mn_tool.getXSLParams(
                mn_tool.getDBXSLOpts({
                    "base.internal": context.portal_url() + \
                                     '/XMLld' + \
                                     '/' + '/'.join(traverse_subpath),
                    ## breaks '#name' links
                    #"html.base": context.portal_url(),
                })),
            'XSL': 'page',
            'DOC_URL': url,
            'DB_XSL': mn_props.getProperty('DB_XSL'),
            'LD2DB_XSL': mn_props.getProperty('LD2DB_XSL'),
        }

        query = (str(context.xq_XMLld) % mn_tool.getQueryParams(params_dict,
                                                              self.request))

        if DevelopmentMode:
            logger.info('\nREQUEST\n' + query)

        da = mn_tool.getDA()

        try:
            res = da.query(query, object_only=1)
        except Fault, error:
            return error

        if DevelopmentMode:
            if str(res):
                logger.info('\nRESULTS\n' + str(res))
            else:
                logger.info('\nNO RESULT\n')

        ## we need to remove unwanted html tags (html, head, body)
        html_purged = (str(res).split('\n')[5:-3]).join('\n')
        return html_purged

class XMLPDFCONV(BrowserView):

    def get_pdf(self, traverse_subpath):
        self.traverse_subpath = traverse_subpath
        htmltext = _HTML_HEADER + ViewPageTemplateFile('templates/XMLPDF.pt')(self)

        # convert to pdf
        pdf = StringIO()
        pisa.showLogging()
        #pdfpisa = pisa.CreatePDF(htmltext,pdf)
        pdfpisa = pisa.CreatePDF(htmltext,pdf,xhtml = False)
        pdf.seek(0)
        return pdf.getvalue()
