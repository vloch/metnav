##parameters=date

cemois = DateTime().strftime("%Y-%m")

if date >= cemois:
  if DateTime().month() == 1:
    last_annee  = DateTime().year() - 1
    last_mois   = 12
  else:
    last_annee  = DateTime().year()
    last_mois   = DateTime().month() - 1

  date = "%s-%02i" % (last_annee, last_mois)

return date