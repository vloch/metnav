# -*- coding: utf-8 -*-
## Copyright (C) 2009 Ingeniweb - Alter Way Solutions - all rights reserved
## No publication or distribution without authorization.

from Globals import DevelopmentMode
from logging import getLogger

from DateTime import DateTime
from Products.Five import BrowserView


from plone.memoize.view import memoize
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
#from zope.component.hooks import getSite

from metnav.functions import myGetSearchableText

import re

tag = re.compile(r"<[^>]+>")

logger = getLogger("MetNav Search View")

class SearchableText:

    def __init__(self, page):
        self.page = page

    def getSearchableText(self):
        text = self.page.getSource()
        if isinstance(text, str):
            text = unicode(self.page.source, 'utf-8')
        # else:
        #   text was already Unicode, which happens, but unclear how it
        #   gets converted to Unicode since the ZPTPage stores UTF-8 as
        #   an 8-bit string.

        if self.page.content_type.startswith('text/html'):
            text = tag.sub('', text)

        return [text]

class Search(BrowserView):

    def absolute_url(self):
        return (self.context.absolute_url() + '/' + self.__name__).encode('utf-8')

class SearchExist(BrowserView):

    def search(self, SearchableText='', title='', description='', creator='', contributeur='', data_type=[], parDate='', choixCritere='', sort_on='score', sort_order='reverse', path=[], xml_type=[], fuzzy=0, **kw):


        pp_tool = getToolByName(self.context, 'portal_properties')
        mn_tool = getToolByName(self.context, 'portal_metadataNav')
        portal  = getToolByName(self.context,"portal_url").getPortalObject()

        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.site_url = self.portal_state.portal_url()
        self.collections = pp_tool.metnav_properties.getProperty('COLLECTIONS')
        self.resource_url = pp_tool.metnav_properties.getProperty('RESOURCE_URL')

        # first, retrieve eXist DB object
        base = mn_tool.getDA()

        try:
            PCT_MIN_RECHERCHE = context.pct_min_recherche
        except:
            PCT_MIN_RECHERCHE = 5

        if SearchableText.strip() == '' and title.strip() == '' and description.strip() == '' and creator.strip() == '' and contributeur.strip() == '' and len(data_type)==0 and len(kw) == 0:
            return []

        # Si une collection (ou plusieurs) est demandée, on l'intègre à la requête
        if DevelopmentMode:
            logger.info(path)
        if path != []:
            COLLECTIONS = "xcollection('%s')" % "', '".join(path)
        else :
            #/|Chebocar|/db/classification/Chebocar.xml|/db/csphysique/metadata
            #root_path|name|exist_path|db_to_use_with
            COLLECTIONS = "collection('%s')" % self.collections[0].split('\n')[0].split('|')[3]

        MOTSCLES = ""
        #if fuzzy == 0 and SearchableText.strip() != "":
        if fuzzy == 0 and SearchableText.strip() != "":
            termes=SearchableText.strip()
            if termes.find('AND')==-1 and termes.find('+')==-1 and termes.find('OR')==-1:
                termes=termes.replace(' ', ' ')
            MOTSCLES = '"' + SearchableText.strip() + '"'
            SEARCHABLETEXT ="""[ft:query(., "%s") or fn:matches(., "%s")]""" % (termes, myGetSearchableText(termes))
             
             
           # Texte à rechercher
        elif fuzzy==1 and SearchableText.strip() != "":
            st = SearchableText.strip()
            liste_rech = []
            liste_terms = []
            for mot in st.split():
                liste_rech.append("""(text:fuzzy-match-any(., "%s"))""" % (mot))
                liste_terms.append("""string-join(distinct-values(text:fuzzy-index-terms("%s")), " ")""" % mot)
            SEARCHABLETEXT= "[" + " intersect ".join(liste_rech) + "]"
            if len(liste_terms) > 1:
                MOTSCLES = "concat(" + ', " ", '.join(liste_terms)  + ', " ")'
            else:
                MOTSCLES = "".join(liste_terms)

        else :
            st=""
            SEARCHABLETEXT=""


        # Recherches spécifiques dans des balises
        SPTAGS = ""
        if title.strip() !="":
            MOTSCLES = '"' + title.strip() + '"'
            SPTAGS +="""[contains(lom:general/lom:title/lom:string/text(), "%s")]""" % title
        if description.strip() !="":
            MOTSCLES = '"' + description.strip() + '"'
            SPTAGS +="""[contains(lom:general/lom:description/lom:string/text(), "%s")]""" % description
        if parDate.strip() !="":
            MOTSCLES = '"' + parDate.strip() + '"'
            if choixCritere=="0":
                SPTAGS +="""[contains(lom:lifeCycle/lom:contribute[lom:role/lom:value='publisher']//lom:dateTime/text(), "%s")]""" % parDate
            elif choixCritere=="1":
                SPTAGS +="""[lom:lifeCycle/lom:contribute[lom:role/lom:value='publisher']//lom:dateTime/text() <= "%s-12-31"]""" % parDate
            elif choixCritere=="2":
                SPTAGS +="""[lom:lifeCycle/lom:contribute[lom:role/lom:value='publisher']/lom:date/lom:dateTime/text() >= "%s-01-01"]""" % parDate
        if creator.strip() !="":
            MOTSCLES = '"' + creator.strip() + '"'
            SPTAGS +="""[contains(lom:lifeCycle/lom:contribute[lom:role/lom:value="author"]/lom:entity/text(), "%s")]""" % creator
        if contributeur.strip() !="":
            MOTSCLES = '"' + contributeur.strip() + '"'
            SPTAGS +="""[contains(lom:lifeCycle/lom:contribute/lom:entity/text(), "%s")]""" % contributeur

        types=""
        if len(data_type) !=0:
            MOTSCLES = '" "'
            if len(data_type)==1:
                types += """[.//lomfrens:value="%s"]""" % str(data_type[0]).strip()
            else:
                i = 0
                types +="["
                while i<len(data_type):
                    if i!=len(data_type)-1:
                        types += """(.//lomfrens:value="%s") or """ % str(data_type[i]).strip()
                    else:
                        types += """(.//lomfrens:value="%s")]""" % str(data_type[i]).strip()
                    i = i + 1

        else:
            types=""

        # Ordre
        if sort_on.strip() != '':
            ORDER = "order by $%s" % sort_on
            if sort_order.strip() == 'reverse':
                ORDER += " descending"
            else:
                ORDER += " ascending"
            ORDER = "order by $score[1] descending, $date[1] descending, $title[1] ascending empty least"

            # Informations sur la base eXist
            BASE = "xmldb:exist://%s" % base.server

            requete = str(self.context.xq_base_lom) % {
			        'site_url':self.site_url,
					'resource_url':self.resource_url,
			        'xquery_version': mn_tool.getXQueryVersion(),
			}
            requete = requete.replace('$COLLECTIONS', COLLECTIONS)
            requete = requete.replace("$SEARCHABLETEXT", SEARCHABLETEXT)
            requete = requete.replace("$TYPES", types)
            requete = requete.replace('$TAGSTOQUERY', SPTAGS)
            requete = requete.replace('$ORDER', ORDER)
            requete = requete.replace('$BASE', BASE)
            requete = requete.replace('$MOTSCLES', MOTSCLES)
            self.context.plone_log(requete)
            res_str = base.query(requete)
            liste_dico = res_str.getDict()
            retour = []
            for dico in liste_dico:
                if int(float(dico['res/score'][0])) > PCT_MIN_RECHERCHE:
                    retour.append(dico)

            if len(retour) == 0 and len(liste_dico) > 0:
                return liste_dico

        return retour

    def getSousType(self, objet = None):
        if objet is None:
            return ''

        VALUE_SEP  = "="                       # séparateur des valeurs/sous types
        LIST_IN    = self.context.soustypes_objets  # variable à lire. Doit être de type lines

        retour = {}

        # Suppression des lignes incorrectes et création de la liste de couples valeur/titre
        for ligne in LIST_IN:
            ligne_norm = ligne.strip()
            if ligne_norm.find(VALUE_SEP) > 0:
                cle, valeur = ligne_norm.split(VALUE_SEP)
                if retour.has_key(cle):
                    retour[cle] = retour[cle] + valeur
                else:
                    retour[cle] = valeur


        if objet in retour.keys():
            return retour[objet]

        return objet

    def getLockedIconTag(self, url):
        URL_LOCKED = ['Area51', 'acces_pro', 'data/profs']

        for url_locked in URL_LOCKED:
            if url_locked in url:
                return """<img src="lock_icon.gif" height="16" width="16" alt="locked" />"""
        return ''


class SearchAdvanced(BrowserView):

    def getObjets(self, titre=None, valeur=None):
        # Ce script lit le contenu d'une variable LIST_IN (créée dans les propriétés du dossier)
        # et transforme les valeurs contenues dans celui-ci
        # en une liste de dictionnaires qui peuvent servir
        # à remplir une combobox

        VALUE_SEP  = "="                     # séparateur des valeurs/titres
        LIST_IN    = self.getTypeObjets()    # variable à lire. Doit être de type lines
        KEY_VALEUR = "valeur"                # nom de la clé des valeurs dans le dictionnaire produit
        KEY_TITRE  = "titre"                 # nom de la clé des titres dans le dictionnaire produit

        retour = []

        # Suppression des lignes incorrectes et création de la liste de couples valeur/titre
        lst_opts = []
        for ligne in LIST_IN:
            ligne_norm = ligne.strip()
            if ligne_norm.find(VALUE_SEP) > 0:
                retour.append({KEY_TITRE:ligne_norm.split(VALUE_SEP, 1)[0], KEY_VALEUR:ligne_norm.split(VALUE_SEP, 1)[1]})

        if titre is None and valeur is None:
            return retour

        if not (titre is None):
            for i in retour:
                if i[KEY_TITRE].lower() == titre.strip().lower():
                    return i

        if not(valeur is None):
            for i in retour:
                if i[KEY_VALEUR].lower() == valeur.strip().lower():
                    return i

        return {}

    def getTypeObjets(self):
        #parents_xq = ""
        #for parent in parents:
        #    if parent.strip() != '':
        #        parents_xq += """/vdex:term[vdex:caption/vdex:langstring &= "%s"]""" % parent
        portal = getToolByName(self.context,"portal_url").getParentNode()
        pp = portal.portal_properties
        mn_tool = getToolByName(self.context, 'portal_metadataNav')

        params_dict = {'XSL':"portlet",
                       'PARTS': "/",
                        }

        query = str(self.context.xq_list_taxon) % mn_tool.getQueryParams(params_dict, self.request)

        if DevelopmentMode:
            logger.info(query)

        da = mn_tool.getDA()
        res = da.query(query.encode('utf-8'), object_only=1)

        return str(res)



# type de document ensdocumenttype 10.2
# type d'objet
# type de document /general/documentsType/source/
# CACHE SUR LES PORTLETS VOCABULAIRES
