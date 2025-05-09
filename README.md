# 💻 Classifieur de Bord Politique par Apprentissage Automatique

> Un projet de NLP et de machine learning pour déterminer si un discours appartient à la droite, au centre ou à la gauche de l’échiquier politique.

---

## 📝 Description

Ce projet a pour objectif de **créer et entraîner un classifieur automatique** capable d’identifier l’**orientation politique d’un discours** en le classant selon trois catégories : **droite**, **centre** ou **gauche**.  

---

## 🔍 Données

- **Source** : [Open Data de l'Assemblée nationale](https://data.assemblee-nationale.fr/travaux-parlementaires/debats)
- **Période couverte** : juillet 2024 à mars 2025
- **Structure** : XML
- **Nettoyage** : Suppression des interruptions ou des interventions trop courtes...
- **Répartition finale** :
  - Gauche : 638 documents
  - Centre : 595 documents
  - Droite : 325 documents

---

## 🧪 Méthodologie

1. **Prétraitement**
   - Parsing XML, nettoyage, filtrage
   - Constitution des sous-corpus par classe

2. **Modélisation**
   - Application de plusieurs classifieurs via WEKA :
     - ZeroR (baseline)
     - Naive Bayes & Naive Bayes Multinomial
     - J48 (arbre de décision)
     - SVM (Support Vector Machine)

3. **Évaluation**
   - Validation croisée 10 folds
   - Métriques : Accuracy, Kappa, F1-score et Matrices de confusion
---

## 👥 Contributeurs

- [Keren DAGUE](https://github.com/KerenDague)
- [Maiwenn PLEVENAGE](https://github.com/00parts)
- [Juliette HENRY](https://github.com/juliettehnr)

---
