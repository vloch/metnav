##parameters=types=''

listImgs = []
typesList = types.split(", ")
# on teste si type=="vid\\xc3\\xa9o" => pour regler le probleme accent ans search_exist

img=""
for type in typesList:
    if type=="article":
        img="article.png"
    elif type=="texte":
        img="texte.png"
    elif type=="vid\xc3\xa9o" or type=="vid\\xc3\\xa9o" or type=="vidéo":
        img="type-video.png"
    elif type=="son":
        img="son.png"
    elif type=="image":
        img="type-image.png"
    elif type=="conf\xc3\xa9rence" or type=="conf\\xc3\\xa9rence" or type=="conférence":
        img="conference.png"
    elif type=="lienVersUnAutreSite":
        img="lienversunautresite.png"
    elif type=="t\xc3\xa9l\xc3\xa9chargement" or type=="t\\xc3\\xa9l\\xc3\\xa9chargement" or type=="téléchargement":
        img="telechargement.png"
    elif type=="exp\xc3\xa9rience" or type=="exp\\xc3\\xa9rience" or type=="expérience":
        img="experience.png"
    elif type=="simulation":
        img="simulation.png"
    elif type=="dossier":
        img="dossier.png"
    elif type=="exercice":
        img="exercice.png"
    elif type=="diaporama":
        img="diaporama.png"
    elif type=="question":
        img="question.png"
    elif type=="albumImage":
        img="albumimage.png"
    elif type=="entretien":
        img="entretien.png"

    listImgs.append(img)

return listImgs
