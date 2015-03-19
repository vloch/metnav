##parameters=auteurs=''

listAuteurs = []
listAuteursBrut = auteurs.split('| ')
for auteurBrut in listAuteursBrut:
    auteur8FN = auteurBrut.split('FN:')[1]
    if (auteur8FN.find('\\n')!=-1):
        authorName = auteur8FN.split('\\n')[0]
    elif (auteur8FN.find('\n')!=-1):
        authorName = auteur8FN.split('\n')[0]
    elif (auteur8FN.find('ORG:')!=-1):
        authorName = auteur8FN.split('ORG')[0]
    else:
        authorName = auteur8FN.split('END:')[0]
    listAuteurs.append(authorName)

return listAuteurs
