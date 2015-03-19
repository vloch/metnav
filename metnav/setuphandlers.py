# -*- coding: utf-8 -*-
## Copyright (C) 2009 Ingeniweb - Alter Way Solutions - all rights reserved
## No publication or distribution without authorization.

from Products.CMFCore.utils import getToolByName
from metnav import config

def importFinalSteps(context):
    """ Import all final steps """

    portal = context.getSite()
    if not hasattr(portal, config.TOOL_ID):
        addTool = portal.manage_addProduct[config.PROJECTNAME].manage_addTool
        addTool(config.TOOL_META_TYPE)

