#!/usr/bin/python
# -*- coding: utf-8 -*-
## Copyright (C) 2009 Ingeniweb - Alter Way Solutions - all rights reserved
## No publication or distribution without authorization.

# Changes Docbook paths to be absolute.
# Launch in the root of a Docbook install or pass the path as the first
# argument of this script
# Use this script on a fresh Docbook XSL installation. The script attempts
# to determine if it's the case, but it may fail...

from logging import getLogger

from os import getcwd
from os.path import abspath, isdir, isfile
from re import MULTILINE, compile, sub
from sys import argv, exit

logger = getLogger("Docbook for eXist")

FILES = ('html/docbook.xsl','html/table.xsl','html/verbatim.xsl')

if len(argv) >= 2:
    path = abspath(argv[1])
    logger.info("Docbook XSL in '%s' will be used." % (path))
else:
    path = getcwd()

# are we in a docbook xsl root ?
if not(isdir(path + '/html')) or not(isfile(path + '/VERSION')):
    logger.error("""
    You must launch this script at the root of a docbook xsl tree
    or pass it as the only argument of the script.""")
    exit(1)


# Change paths in each file
pattern = compile("""<xsl:include href="([^\"]*)"/>""", MULTILINE)
for file in FILES:
    f = open(path + '/' + file, 'rt')
    chaines = f.readlines()
    f.close()
    chaines_new = []
    for chaine in chaines:
        NO_PATH = False
        if pattern.findall(chaine):
            url = pattern.findall(chaine)[0]
            if '..' in url:
                urls = url.split('/')
                i = urls.index('..')
                url = '/' + '/'.join(urls[i+1:])
            elif url.count('/') > 2:
                logger.warn("""No modifications to %s (seems already tagged).
Please use a fresh Docbook XSL installation.""" % url)
                NO_PATH = True
            else:
                url = '/html/' + url
            if NO_PATH:
                chaines_new.append(pattern.sub("""<xsl:include href="%s"/>""" \
                                           % url, chaine))
            else:
                chaines_new.append(pattern.sub("""<xsl:include href="%s"/>""" \
                                           % (path + url), chaine))
        else:
            chaines_new.append(chaine)
    f = open(path + '/' + file, 'wt')
    f.writelines(chaines_new)
    f.close()

logger.info("""Changes done. Don't forget to change the property DB_XSL in
portal_properties/metnav_properties once the product is installed in Plone.
It *must* be %s/html/docbook.xsl or your customized version.""" % path)
