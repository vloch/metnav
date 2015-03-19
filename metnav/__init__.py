# -*- coding: utf-8 -*-
## Copyright (C) 2009 Ingeniweb - Alter Way Solutions - all rights reserved
## No publication or distribution without authorization.


# CMF imports
from Products.CMFCore.DirectoryView import registerDirectory
from Products.CMFCore.utils import ToolInit

# Product imports
from metnav.config import *
from metnav.tool import MetadataNavTool

registerDirectory('skins', GLOBALS)
tools = (MetadataNavTool,)


def initialize(context):

    # Register tool
    ToolInit(PROJECTNAME + " Tool",
             tools=tools,
             icon="tool.gif",
              ).initialize(context)
