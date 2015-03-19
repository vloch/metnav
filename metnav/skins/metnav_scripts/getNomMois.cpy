##parameters=num=1

nom_mois=['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
num = int(num)
if num > 12 or num < 1:
  return ''

return nom_mois[num-1]