# -*- coding: utf-8 -*-
## Copyright (C) 2009 Ingeniweb - Alter Way Solutions - all rights reserved
## No publication or distribution without authorization.

# Imports
from Products.CMFCore.permissions import ManagePortal


GLOBALS = globals()
PROJECTNAME = 'metnav'

TOOL_ID = 'portal_metadataNav'
TOOL_META_TYPE = 'MetadataNavTool'
TOOL_TITLE = 'XML Metadata Navigation Tool'



######## STRUCTURE DE LA SKIN ########
#Liste des dossiers dans skins/ à importer dans le Plone à l'installation
SKIN_FOLDERS = ('metnav_images', 'metnav_xquery', 'metnav_scripts', 'metnav_portlets', 'metnav_templates' )

#Nom de la skin générale (en principe, le même nom que le produit) => pas d'espaces ou caractères non ASCII
SKIN_NAME = 'MetNav'

#Nom du site
SITE_NAME = 'Metadata Nav.'

#Skin sur laquelle on se base
BASE_SKIN = 'Plone Default'

#Choix des composants à installer
INSTALL_PROPERTY_SHEET 	= True
INSTALL_TOOL		= True
INSTALL_CONFIGLET	= True
INSTALL_CSS         = True

#Choix des composants à désinstaller
REMOVE_PROPERTY_SHEET 	= INSTALL_PROPERTY_SHEET
REMOVE_TOOL		= INSTALL_TOOL
REMOVE_CONFIGLET	= INSTALL_CONFIGLET
REMOVE_CSS = INSTALL_CSS


######## PROPRIÉTÉS ########
#ID de l'objet qui contient les propriétés de la skin
PROPS_ID = "%s_properties" % (SKIN_NAME.lower())

#Titre  de l'objet qui contient les propriétés de la skin
PROPS_TITLE = "Properties for %s" % (SKIN_NAME)

LIST_PROPS = [
            {'name':'BATCH_LENGTH',
             'value':15,
             'type':'integer',},
            {'name':'COLLECTIONS',
             'value':['/planetterre|ThoKaVi v2.0|/db/classification/Thokavi-2.0_vdex.xml|/db/planetterre/metadata',],
             'type':'lines',},
            {'name':'COLLECTION_METADATA',
             'value':'/db/planetterre/metadata',
             'type':'string',},
            {'name':'RESOURCE_URL',
             'value':'/lom:technical/lom:location[1]/text()',
             'type':'string',},
            {'name':'CONDITION_BASE',
             'value':"""[not(lom:metaMetadata/lom:contribute[lom:role='creator' or lom:role='createur']) or lom:metaMetadata/lom:contribute[lom:role='creator' or lom:role='createur']/lom:date/lom:dateTime/text() <= current-date()]""",
             'type':'string',},
            {'name':'DB_XSL',
             'value':'file:///usr/local/docbook-xsl-ns/html/docbook.xsl',
             'type':'string',},
            {'name':'DB_XSL_OPTS',
             'value':(
                        'html.cleanup=1',
                        'make.valid.html=1',
                        'css.decoration=1',
                        'suppress.navigation=1',
                        'table.frame.border.thickness=0',
                        'l10n.gentext.language=fr',
                        'l10n.gentext.default.language=fr',
                        'generate.index=0',
                        'generate.meta.abstract=0',
                        'draft.mode=0',
                     ),
             'type':'lines',},
            {'name':'DEFAULT_COLLATION',
             'value':"""declare default collation "?lang=fr-FR;strength=primary;decomposition=none";""",
             'type':'string',},
            { 'name':'EXIST_DA',
              'value':'exist',
              'type':'string',},
            {'name':'HEAD_SUP',
             'value':'',
             'type':'text',},
            {'name':'LIMIT_RELATED',
             'value':10,
             'type':'int',},
            {'name':'OBJECTS',
             'value':(
                        'Tout=',
                        'Article=article',
                        'Conf&eacute;rence=conf&eacute;rence',
                        'Exercice=exercice',
                        'Exp&eacute;rience=exp&eacute;rience',
                        'Question du mois=question',
                        'Dossier=dossier',
                        'Simulation=simulation',
                        'Diaporama=diaporama',
                     ),
             'type':'lines',},
            {'name':'MEDIAS',
             'value':(
                        'Tout=',
                        'Image=image',
                        'Vid&eacute;os=vid&eacute;o',
                        'Son=son',
                        'Texte=texte',
                        'T&eacute;l&eacute;chargement=t&eacute;l&eacute;chargement',
                        'Lien vers un autre site=lienVersUnAutreSite',
                     ),
             'type':'lines',},
            {'name':'OBJET_SEMAINE',
             'value':"""[lomfrens:ensData/lomfrens:ensDocumentType/lomfrens:value = "imageDeLaSemaine"]""",
             'type':'string',},
            {'name':'SCORE_CONNEXE',
             'value':15,
             'type':'int',},
            {'name':'TEMPLATE_SEARCH',
             'value':'contains(%s, "%s")',
             'type':'string',},
            {'name':'URL_DOC',
             'value':'/XML',
             'type':'string',},
            {'name':'XPATH_SEARCH_EXPR',
             'value':(
                        'motcle=lom:general/lom:keyword',
                        'titre=lom:general/lom:title',
                        'description=lom:general/lom:description',
                        'auteur=lom:lifeCycle/lom:contribute[lom:role/lom:value="author" or lom:role/lom:value="auteur"]/entity',
                        'niveau=lom:educational/lom:typicalAgeRange',
                        'typederessource=lom:educational/lom:learningResourceType',
                        'classification=lom:classification/lom:taxonPath',
                        'couverture=lom:general/lom:coverage',
                        'st=.',
                        'date=lom:lifeCycle/lom:contribute[lom:role/lom:value="author" or lom:role/lom:value="auteur"]/lom:dateTime',
                     ),
             'type':'lines',},
            {'name':'XSL_CLASS_LIST',
             'value':'xmldb:exist:///db/xsl/class2list_vdex.xsl',
             'type':'string',},
            {'name':'ARCHIVE_MOIS',
             'value':False,
             'type':'boolean',},
            {'name':'INIT_ANNEE',
             'value':2002,
             'type':'int',},
            {'name':'HREF_BLANK',
             'value':True,
             'type':'boolean',},
            ]
"""         {'name':'',
             'value':'',
             'type':'',},


"""


TEMPLATE_SEARCH_SCORE = [{'value':"""count($res/lom:classification/lom:taxonPath[%s])""", 'weight':1},
                         {'value':"""count($res/lom:general/lom:keyword[%s])""", 'weight':2},
                         {'value':"""count($res/lom:general/lom:title[%s])""", 'weight':3},
                        ]

