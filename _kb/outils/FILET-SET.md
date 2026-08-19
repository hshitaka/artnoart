# Filet set — djay

Geste : un set long dans djay, sans la sync iCloud sur le dos.

Cause : [_kb/liens/CAUSE-djay.md](../liens/CAUSE-djay.md).

## Avant le set

1. Ferme djay.
2. Réglages Mac → Apple ID → iCloud → **djay OFF**.
3. Lance le filet (copie la bibliothèque, reset CloudKit, ne supprime rien) :

```bash
cd "/chemin/vers/artnoart"
python3 "_kb/outils/djay_filet.py" avant-set
```

4. Ouvre djay. Joue.

## Après le set

1. Ferme djay, ou laisse-le hors live.
2. Réglages Mac → Apple ID → iCloud → **djay ON**.
3. Rappel :

```bash
cd "/chemin/vers/artnoart"
python3 "_kb/outils/djay_filet.py" apres-set
```

## Voir l’état

```bash
cd "/chemin/vers/artnoart"
python3 "_kb/outils/djay_filet.py" status
```

La copie est dans `Music/djay-backups/`. L’original reste en place.

Pas en live. Pas de `rm`. Pas de nouvelle bibliothèque vide.
