# -*- coding: utf-8 -*-
## Copyright (C) 2009 Ingeniweb - Alter Way Solutions - all rights reserved
## No publication or distribution without authorization.

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime

class res_semaine(BrowserView):

    def update(self):
        pp_tool = getToolByName(self.context, 'portal_properties')
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.site_url = self.portal_state.portal_url()
        self.metadataNav = getToolByName(self.context, 'portal_metadataNav')
        self.meta_url = pp_tool.metnav_properties.getProperty('COLLECTION_METADATA')
        self.typeObjet = pp_tool.metnav_properties.getProperty('OBJET_SEMAINE')
    
    def getImagesDeLaSemaine(self, annee="", fullpath=False):
    
        pp_tool = getToolByName(self.context, 'portal_properties')
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.site_url = self.portal_state.portal_url()
        self.metadataNav = getToolByName(self.context, 'portal_metadataNav')
        self.meta_url = pp_tool.metnav_properties.getProperty('COLLECTION_METADATA')
        self.typeObjet = pp_tool.metnav_properties.getProperty('OBJET_SEMAINE')
        context = self.context
        exist = context.exist
        meta_url = self.meta_url
        
        if annee != "":
            anneeCondition = """[contains(lom:lifeCycle/lom:contribute[lom:role/lom:value='publisher']/lom:date/lom:dateTime/text(), "%s")]""" % annee
        else:
            anneeCondition=""
        
        mn_tool = getToolByName(self.context, 'portal_metadataNav')
        
        query = self.context.xq_imageSemaine.__str__() % {
            'meta_url':meta_url,
            'site_url': self.site_url,
            'OBJECT_TYPE' : self.typeObjet,
            'ANNEE':anneeCondition,
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

    def absolute_url(self):
        return (self.context.absolute_url() + '/' + self.__name__).encode('utf-8')

    def annee_semaine(self, year='', template_url='', output='year_list'):
        context = self.context
        mn_tool = getToolByName(context, 'portal_metadataNav')
        mn_props = getToolByName(context, 'portal_properties').metnav_properties

        params_dict = {'XSL':output,
                        'XSL_PARAMS':{'template.url':template_url,
                                    'current.year':year,
                                    'rss.title':"Semaine",
                                    'rss.desc':'Une ressource de la semaine',
                                    'rss.copyright':'Mon établissement',},
                        'COLLATION':'',
                        'OBJECT_TYPE':mn_props.getProperty('OBJET_SEMAINE', '[lom:educational/lom:learningResourceType &= "figure"]'),
                    }

        query = (str(context.xq_semaine_annee_index) % mn_tool.getQueryParams(params_dict, context.REQUEST))

        da = mn_tool.getDA()

        res = da.query(query, object_only=1)
        context.plone_log('as', str(res))
        return str(res)

    def list_semaine(self, year=None, output='table'):
        context = self.context
        mn_tool = getToolByName(context, 'portal_metadataNav')
        mn_props = getToolByName(context, 'portal_properties').metnav_properties

        if year == None:
            year = int(DateTime().year())
        else:
            year = int(year)

        params_dict = {'XSL':output,
                        'XSL_PARAMS':{'rss.title':"Semaine",
                                    'rss.desc':'Les ressources de la semaine',
                                    'rss.copyright':'Mon établissement',},
                        'COLLATION':'',
                        'OBJECT_TYPE':mn_props.getProperty('OBJET_SEMAINE', '[lom:educational/lom:learningResourceType &= "figure"]'),
                        'LIMITS':'[contains(lom:metaMetadata/lom:contribute[lom:role="creator" or lom:role="createur"]/lom:date/lom:dateTime, "%u")]' % (year),
                    }

        query = (str(context.xq_semaine_index) % mn_tool.getQueryParams(params_dict, context.REQUEST))

        da = mn_tool.getDA()

        res = da.query(query, object_only=1)

        return str(res)

