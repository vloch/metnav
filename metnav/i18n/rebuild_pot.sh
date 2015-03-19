#!/bin/sh
# This file must be placed and executed in the i18n subdirectory of a Plone product.
TEMPLATES=`find ../ -iregex '.*\..?pt'`
# Change next line !
DOMAIN="metnav" 
FILEFILTER="/home/spilloz/Prog/zope/develmetnav/Products/PloneTranslations/i18n/plone.pot"
i18ndude rebuild-pot --pot $DOMAIN-tmp.pot  --create $DOMAIN $TEMPLATES 2> report.txt
i18ndude filter $DOMAIN-tmp.pot $FILEFILTER > $DOMAIN.pot 
for lang in "fr" "en";do
    if [ ! -f $DOMAIN-$lang.po ]
    then
        touch $DOMAIN-$lang.po
    fi
    i18ndude sync --pot $DOMAIN.pot $DOMAIN-$lang.po
    # Next line if i18ndude forgets some i18n...
    #cat missing-$lang.po.templ >> $DOMAIN-$lang.po 
done
