# Audit DWET — ARTNOART

Date : 17 août 2026  
Périmètre : code, interface, et voies de téléchargement du dépôt `hshitaka/artnoart`.

## Verdict

Le site d’origine n’était pas publiable : HTML cassé, CSS/JS vides, navigation factice, aucun fichier à télécharger. L’audit a conduit à une reconstruction ciblée (même stack : HTML / CSS / JS) plutôt qu’à un empilement de rustines.

## Constats d’origine

### Code

| Gravité | Problème |
| --- | --- |
| Haute | `index.css` et `index.js` vides alors que le projet les déclare |
| Haute | `script src="script.js"` pointe vers un fichier inexistant |
| Haute | Meta viewport invalide : `widt=device-with` |
| Moyenne | CSS inline dans le `body`, styles hors `head` |
| Moyenne | `gitignore` mal nommé et vide ; `.DS_Store` versionné |
| Moyenne | README recopié six fois, titre de page `Document` |
| Basse | `lang="en"` pour un contenu mixte FR/EN |
| Basse | Liens `href="#"` sans sections |

### UI

- Fond aqua, header beige, titre rouge en `fantasy` : contraste et identité illisibles.
- Nav sans état actif, sans menu mobile, sans skip-link.
- Aucune hiérarchie réelle (un `h2` « changement », un `p` « texte »).
- Pas d’écoute, pas de téléchargement, pas de pied de page, pas de favicon.

### Téléchargement

Aucune voie n’existait : pas de fichiers, pas d’attribut `download`, pas d’API `fetch`.

## Corrections appliquées

- Viewport, langue, titre, description, favicon, CSS/JS externes.
- Structure sémantique : `header` / `nav` / `main` / sections `#home` `#prod` `#mix` / `footer`.
- Navigation sticky, état `aria-current`, menu mobile, skip-link, `prefers-reduced-motion`.
- Lecteur audio (un extrait à la fois).
- Module **DWET** : voie **directe** (`a[download]`) et voie **fetch** (`Blob` + Object URL).
- Catalogue JSON + fichiers démo WAV/TXT.
- `.gitignore` correct, README réel.

## UI après correction

Direction visuelle atelier / console (fond charbon, signal cyan, méta en mono). Les listes Prod et Mix exposent lecture + les deux boutons de téléchargement. Les extraits WAV sont des jingles techniques, pas un catalogue discographique.

## Tests des voies

Commande : `python3 tests/test_downloads.py`

Résultat : **9/9 OK** après correctif lecture.

Couverture :

1. Chaque entrée de `catalog.json` existe et a la taille déclarée.
2. Voie HTTP directe : `GET` 200, corps identique au disque.
3. `HEAD` et `GET` exposent la même longueur.
4. HTML référence bien `index.css` / `index.js`, plus `script.js`, viewport corrigé, `data-dwet-mode` direct + fetch, attribut `download` sur chaque fichier.
5. Les WAV commencent par `RIFF` / `WAVE`.
6. Une URL inconnue répond 404.

## Correctif lecture (après QA navigateur)

Les téléchargements Direct et Fetch étaient bons. La lecture échouait visuellement parce que les extraits duraient ~1 s : l’événement `ended` vidait `audio.src`, ce qui déclenchait un faux `error` (« Lecture impossible »). L’état cyan disparaissait tout de suite.

Correctifs : extraits à 5 s, arrêt sans vider `src`, bordure cyan nette, logo cliquable, focus plus visible.

- Les extraits WAV durent 5 secondes (jingles techniques, pas des masters).
- Pas de backend : pas de compteur de téléchargements ni d’auth.
- Les polices Google Fonts nécessitent le réseau au premier chargement.
- Le mixeur à droite de la section Mix est décoratif.
