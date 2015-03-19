## Script (Python) "getArchives"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=
##
from DateTime import DateTime

request = context.REQUEST
affiche_mois = context.portal_properties.metnav_properties.ARCHIVE_MOIS
first_annee = context.portal_properties.metnav_properties.INIT_ANNEE
last_annee  = DateTime().year()
selectAnnee = request.get("date_annee", last_annee)
selectMois = request.get("archives-mois", "")
first_mois  = 1
anneeEcoulee= last_annee+1

if affiche_mois==True:
    if DateTime().month() == 1:
      last_month  = 12
    else:
      last_month  = DateTime().month() - 1

    res = """<form name="archives" method="get" action=""><fieldset><label for='date_annee'>Sélectionner l'année : </label><select name="date_annee">"""
    while anneeEcoulee > first_annee:
        anneeEcoulee = anneeEcoulee - 1
        if int(anneeEcoulee)==int(selectAnnee):
            res +="<option value='%s' selected='selected'>%s</option>" % (anneeEcoulee, anneeEcoulee)
        else:
            res +="<option value='%s'>%s</option>" % (anneeEcoulee, anneeEcoulee)

    res += """</select>, <label for='archives-mois'>un mois : </label> <select name="archives-mois"><option value=''>Tous</option>"""

    for mois in range(1, 13):
        moisDouble="%02i" % mois
        if moisDouble==selectMois:
            res += """<option value="%02i" selected="selected">%s</option>""" % (mois, container.getNomMois(mois))
        else:
            res += """<option value="%02i">%s</option>""" % (mois, container.getNomMois(mois))
       

    return res + "</select><input type='submit' value='Ok'/></fieldset</form>"
else:
    res = """<form name="archives" method="get" action=""><fieldset><label for='select'>Sélectionner l'année : </label><select name="date_annee">"""
    while anneeEcoulee > first_annee:
        anneeEcoulee = anneeEcoulee - 1
        if int(anneeEcoulee)==int(selectAnnee):
            res +="<option value='%s' selected='selected'>%s</option>" % (anneeEcoulee, anneeEcoulee)
        else:
            res +="<option value='%s'>%s</option>" % (anneeEcoulee, anneeEcoulee)

    res += """</select><input type='submit' value='Ok'/></fieldset></form>"""

    return res