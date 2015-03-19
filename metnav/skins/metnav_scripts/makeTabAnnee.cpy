##parameters=annee, mois_debut=1, mois_fin=12

row = ""
for mois in range(1, 7):
  if (mois >= mois_debut) and (mois <= mois_fin):
    lien = """<a href="res_archives?date_archives=%s-%02i">%s</a>""" % (str(annee), mois, container.getNomMois(mois))
  else:
    lien = """%s""" % (container.getNomMois(mois))
  row += """<tr><td>%s</td>""" % lien

  if ((mois+6) >= mois_debut) and ((mois+6) <= mois_fin):
    lien = """<a href="res_archives?date_archives=%s-%02i">%s</a>""" % (str(annee), (mois+6), container.getNomMois((mois+6)))
  else:
    lien = """%s""" % (container.getNomMois((mois+6)))
  row += """<td>%s</td></tr>""" % lien

tableau ="""<table>
<th>Année %s</th>
%s
</table>
""" % (str(annee), row)

return tableau
