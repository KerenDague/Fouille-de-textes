import xml.etree.ElementTree as ET
import os
import re
import argparse



def parse_xml(fichier):

    with open(fichier, "r", encoding='utf-8') as f:
        all_discours = []

        texte = f.read()

        points = re.findall(r'<point(.*?)</point>', texte, re.S)

        for point in points:
            paragraphes = re.findall(r'<paragraphe.*</paragraphe>', point, re.S)
            for paragraphe in paragraphes:
                if 'code_grammaire="PAROLE_GENERIQUE"' in paragraphe:
                    nom = str(re.findall(r"<nom>.*</nom>", paragraphe))
                    nom_clean = str(re.sub(r"</?nom>", r"", nom))

                    texte = str(re.findall(r"<texte stime.*</texte>", paragraphe))
                    texte_clean = str(re.sub(r"</?texte>", r"", texte))
                    texte_clean = str(re.sub(r'<texte stime="(.*?)">', r"", texte_clean))
                    texte_clean = str(re.sub(r"\\xa0", r"", texte_clean))
                    texte_clean = str(re.sub(r"(n)?<exposant>(.|..|...)?</exposant>", r"", texte_clean))
                    texte_clean = str(re.sub(r"<br/>", r"", texte_clean))
                    texte_clean = str(re.sub(r"(<italique>.*</italique>|<italique/>)", r"", texte_clean))
                    texte_clean = str(re.sub(r"(\\t)+", r"", texte_clean))

                    discours = {'source' : os.path.basename(fichier), 'orateur': nom_clean, 'texte': texte_clean}
                    all_discours.append(discours)

                else :
                    pass




        return all_discours
'''
    try:
        tree = ET.parse(fichier)
    except ParseError :
        return False

    root = tree.getroot()

    all_discours = []

    for item in root.findall("point"):
        nom = item.find("nom").text if item.find("nom") is not None else " "
        texte = item.find("texte").text if item.find("texte") is not None else " "

        discours = {'source' : fichier, 'orateur': nom, 'texte': texte}
        all_discours.append(discours)

    return all_discours
'''

def lire_corpus_os(dossier_chemin):

    fichiers_xml = []

    for element in os.listdir(dossier_chemin):
        chemin_complet = os.path.join(dossier_chemin, element)
        if os.path.isdir(chemin_complet):
            fichiers_xml.extend(lire_corpus_os(chemin_complet))
        elif os.path.isfile(chemin_complet) and chemin_complet.endswith(".xml"):
            fichiers_xml.append(chemin_complet)

    return fichiers_xml


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

    for fichier in liste:
        print(f'source: {fichier.get('source','')}')
        print(f'orateur: {fichier.get('orateur','')}')
        print(f'texte: {fichier.get('texte','')}')
        print('\n')
