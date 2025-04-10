import xml.etree.ElementTree as ET
import os
import re
import argparse
from pathlib import Path

def parse_xml(fichier):

    with open(fichier, "r", encoding='utf-8') as f:

        all_discours = []

        texte = f.read()

        points = re.findall(r'<point(.*?)</point>', texte, re.S)


        for point in points:
            paragraphes = re.findall(r'<paragraphe(.*?)</paragraphe>', point, re.S)
            for p in paragraphes:

                code = str(re.search(r'code_grammaire="(.*)" ', p))
                code_parole = "PAROLE_GENERIQUE"
                #code_disc = "DISC_ARTICLES"

                if code_parole in code:

                    nom = str(re.findall(r"<nom>.*</nom>", p))
                    mauvais_code = "président"

                    if mauvais_code not in nom:

                        texte = str(re.findall(r"<texte stime.*</texte>", p))

                        if len(texte) >= 2000 :

                            code = code

                            nom = str(re.findall(r"<nom>.*</nom>", p))
                            nom_clean = str(re.sub(r"</?nom>", r"", nom))


                            texte_clean = str(re.sub(r"</?texte>", r"", texte))
                            texte_clean = str(re.sub(r'<texte stime="(.*?)">', r"", texte_clean))
                            texte_clean = str(re.sub(r"\\xa0", r" ", texte_clean))
                            texte_clean = str(re.sub(r"(n)?<exposant>(.|..|...)?</exposant>", r"", texte_clean))
                            texte_clean = str(re.sub(r"<br/>", r"", texte_clean))
                            texte_clean = str(re.sub(r"(<italique>(.*?)</italique>|<italique/>)", r"", texte_clean))
                            texte_clean = str(re.sub(r"(\\t)+", r"", texte_clean))

                            discours = {'source' : os.path.basename(fichier), 'code': code, 'orateur': nom_clean, 'texte': texte_clean}
                            all_discours.append(discours)

                        else:
                            pass

                    else :
                        pass

                else:
                    pass

        return all_discours


def lire_corpus_os(dossier_chemin):

    fichiers_xml = []

    for element in os.listdir(dossier_chemin):
        chemin_complet = os.path.join(dossier_chemin, element)
        if os.path.isdir(chemin_complet):
            fichiers_xml.extend(lire_corpus_os(chemin_complet))
        elif os.path.isfile(chemin_complet) and chemin_complet.endswith(".xml"):
            fichiers_xml.append(chemin_complet)

    return fichiers_xml


def trier_tendance(textes: list[dict]) :

    with open("deputes_gauche.txt", "r") as f :
        orateurs_gauche = f.read()
    with open("deputes_droite.txt", "r") as f :
        orateurs_droite = f.read()
    with open("deputes_centre.txt", "r") as f :
        orateurs_centre = f.read()

    i = 1
    
    dossier_gauche = "./gauche"
    dossier_droite = "./droite"
    dossier_centre = "./centre"
    
    for texte in textes :

        orateur = texte["orateur"].translate(str.maketrans('', '', "[']"))
        texte_orateur = texte["texte"].translate(str.maketrans('', '', "[']"))

        if orateur in orateurs_gauche :       
            with open(f"{dossier_gauche}/{i}.txt", "w") as f :
                f.write(f"{texte_orateur}")
           
        elif orateur in orateurs_centre :
            with open(f"{dossier_centre}/{i}.txt", "w") as f :
                f.write(f"{texte_orateur}")

        elif orateur in orateurs_droite :
            with open(f"{dossier_droite}/{i}.txt", "w") as f :
                f.write(f"{texte_orateur}")
        
        i +=1


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dossier", type=str)
    args = parser.parse_args()

    dossier_chemin = args.dossier

    all_fichiers = lire_corpus_os(dossier_chemin)

    liste = []

    for file in all_fichiers:

        resultat = parse_xml(file)
        liste.extend(resultat)

    trier_tendance(liste)

    '''for fichier in liste:
        print(f'source: {fichier.get('source','')}')
        print(f'code: {fichier.get('code','')}')
        print(f'orateur: {fichier.get('orateur','')}')
        print(f'texte: {fichier.get('texte','')}')
        print('\n')'''