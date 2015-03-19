#-*-coding: iso-8859-1 -*-

def myGetSearchableText(SearchableText='', repl_acc=1):

    # Constantes
    DICT_ACC = {'a':'[aàâä]', 'à':'[aàâä]', 'â':'[aàâä]', 'ä':'[aàâä]',
                'e':'[eéèêë]', 'é':'[eéèêë]', 'è':'[eéèêë]', 'ê':'[eéèêë]', 'ë':'[eéèêë]',
                'i':'[iîï]', 'î':'[iîï]', 'ï':'[iîï]',
                'o':'[oôö]', 'ô':'[oôö]', 'ö':'[oôö]',
                'u':'[uùûü]', 'ù':'[uùûü]', 'û':'[uùûü]', 'ü':'[uùûü]',
                'c':'[cç]', 'ç':'[cç]',
               }

    CAR_INT = '.?'
    CAR_FIN = 'rsx'
    CAR_FIN_REMP = '[ersx]?'
    CAR_SUP = 'eéiurstx'
    SEPARATEUR = " "
    LISTE_IGNORE = ["a","au","aux","de","des","du","d'","le","l'","la","les","et","ou","pour","se","s'","ses","dans","car","or","ni","en", "y", "par"]
    LISTE_DEBUT_IGNORE = ["l'", "d'"] # débuts de mots à ignorer
    AJOUT_DEBUT_VOYELLE = "[cdls]?[']?"

    SearchableText = SearchableText.decode('utf8').encode('iso8859-1')
    #SearchableText = unicode(SearchableText)
    # Options par défaut
    if SearchableText.strip() == '':
        return ""


    nv_st = ""

    # Suppression des termes communs qui n'ont pas de signification pour la recherche
    lst_tmp = SearchableText.strip().split(SEPARATEUR)
    for mot_ignore in  LISTE_IGNORE :
        if mot_ignore in lst_tmp:
            lst_tmp.remove(mot_ignore)
    for deb_mot in LISTE_DEBUT_IGNORE:
        for mot in lst_tmp:
            if mot[:len(deb_mot)] == deb_mot:
                lst_tmp.remove(mot)
                lst_tmp.append(mot[len(deb_mot):])

    lst_st = []
        
    st = SEPARATEUR.join(lst_tmp)
        
    if repl_acc:
        for mot in st.split(SEPARATEUR):
            nv_st = ""
            i = 0
            for car in mot:
                if (i == 0) and (car in DICT_ACC.keys()):
                    nv_st = AJOUT_DEBUT_VOYELLE
                if i == len(mot)-1:
                    if car in CAR_SUP:
                      nv_st += CAR_FIN_REMP 
                    else:
                        nv_st += DICT_ACC.get(car, car)
                else:
                    nv_st += DICT_ACC.get(car, car)
                i += 1

            nv_st += CAR_INT

            lst_st.append(nv_st.strip())
    else:
        lst_st = lst_tmp


 
  
    nv_st = SEPARATEUR.join(lst_st)

    return nv_st.decode('iso8859-1').encode('utf8')

