##parameters=

affiche_mois = context.portal_properties.metnav_properties.ARCHIVE_MOIS
first_annee = context.portal_properties.metnav_properties.INIT_ANNEE
first_mois  = 1

if affiche_mois==True:
    if DateTime().month() == 1:
      last_annee  = DateTime().year() - 1
      last_month  = 12
    else:
      last_annee  = DateTime().year()
      last_month  = DateTime().month() - 1

    res = """<table width="100%">"""
    for annee in range(first_annee, last_annee + 1):
      first = 1
      last = 12
      if annee == first_annee:
        first = first_mois
      if annee == last_annee:
        last = last_month

      if (annee - first_annee) % 2 == 0:
        res += "<tr><td>" + container.makeTabAnnee(annee, first, last) + "</td>"
      else:
        res += "<td>" + container.makeTabAnnee(annee, first, last) + "</td></tr>"

    if (last_annee - first_annee) % 2 == 1:
      res = res + "</tr>"

    return res + "</table>"+str(affiche_mois)
else:
    last_annee  = DateTime().year() - 1
    res = """<table width="100%">"""
    for annee in range(first_annee, last_annee + 1):
       res += "<tr><td><a href='res_archives?date_archives=%s'>%s</a></td></tr>" % (str(annee), str(annee))
#      if (annee - first_annee) % 2 == 0:
#        res += "<tr><td><a href='res_archives?date_archives=%s'>%s</a></td></tr>" % (str(annee), str(annee))
#      else:
#        res += "<td><a href='res_archives?date_archives=%s'>%s</a></td></tr>" % (str(annee), str(annee))

    if (last_annee - first_annee) % 2 == 1:
      res = res + "</tr>"

    return res + "</table>"

