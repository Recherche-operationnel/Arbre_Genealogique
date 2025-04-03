# 🌳 Arbre Généalogique - Projet Scolaire


*Application web développée en JavaScript pour le cours de Recherche Opérationnelle*

---

## 📌 Table des Matières
- [Description](#-description)
- [Fonctionnalités](#-fonctionnalités)
- [Technologies](#-technologies)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Structure du Projet](#-structure-du-projet)
- [Aperçu](#-aperçu)
- [Auteurs](#-auteurs)

---

## 📝 Description
Application web permettant de **créer et visualiser** un arbre généalogique complet avec :
- Gestion des relations familiales (parents/enfants/conjoints)
- Système de sauvegarde/chargement
- Interface intuitive et responsive

**Contexte** : Projet réalisé dans le cadre du cours de Recherche Opérationnelle.

---
```mermaid
classDiagram
    %% Classes principales
    class Personne {
        +id: Number
        +prenom: String
        +nom: String
        +dateNaissance: Date
        +dateDeces: Date
        +genre: String
        +photo: String
        +notes: String
        +parents: Personne[]
        +conjoint: Personne
        +enfants: Personne[]
        +ajouterParent()
        +ajouterEnfant()
        +definirConjoint()
    }

    class ArbreGenealogique {
        +membres: Personne[]
        +racines: Personne[]
        +ajouterMembre()
        +supprimerMembre()
        +trouverMembre()
        +genererArbre()
        +sauvegarderJSON()
        +chargerJSON()
    }

    class InterfaceUtilisateur {
        -arbre: ArbreGenealogique
        +afficherArbre()
        +afficherFormulaire()
        +gererClicCarte()
        +afficherModal()
    }

    %% Relations
    Personne "1" *-- "0..2" Personne : Parents
    Personne "1" -- "0..1" Personne : Conjoint
    Personne "1" *-- "0..*" Personne : Enfants
    
    ArbreGenealogique "1" *-- "0..*" Personne : Contient
    InterfaceUtilisateur --> ArbreGenealogique : Utilise
```

## 🎯 Fonctionnalités
### 🌟 Principales
- ✅ Visualisation hiérarchique de la famille
- ✅ Ajout/modification/suppression des membres
- ✅ Gestion des relations complexes
- ✅ Export/import au format JSON

### ✨ Bonus
- 🎨 Design coloré par genre
- 📱 Compatible mobile
- ➕ Ajout rapide d'enfants

---

## 💻 Technologies
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow?logo=javascript)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3)

### Classes UML pour ce système d'arbre généalogique

