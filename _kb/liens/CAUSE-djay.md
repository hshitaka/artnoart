# Cause — djay plante au bout d’un moment

C’est un **bug logiciel d’Algoriddim djay**, pas un problème de carte kb-liens.

## La cause

Pendant le set, djay écrit sans arrêt dans sa bibliothèque (analyse, cues, Neural Mix / mashup). **iCloud (CloudKit) essaie de synchroniser ça en live.**

Au bout de 2 à 4 heures, la sync sature le processeur. L’app devient lente, puis plante — ou la musique s’arrête.

Le fichier en cause : `djay Media Library.djayMediaLibrary` (souvent `~/Music/djay/`). Il gonfle. CloudKit n’arrive plus à suivre.

Algoriddim l’a reconnu : ralentissement lié à la sync iCloud, CPU qui monte au-dessus de 120 % après quelques heures, crash après 2–3 h de set. Même geste que le tien : mashup live dans djay, longtemps.

## Ce que ce n’est pas

- Pas un mauvais dessin du losange.
- Pas le piège refresh S136 (`import_djay_data.py`) — ça, c’est a2dd qui lit djay, un autre chantier.
- Neural Mix / mashup aggrave la RAM, mais ce n’est pas l’horloge qui tue l’app. L’horloge, c’est iCloud qui sync la bibliothèque pendant que tu joues.

## Pour verrouiller (chez toi)

1. djay ouvert → Réglages Mac : iCloud est-il coché pour djay ?
2. Taille du fichier `djay Media Library.djayMediaLibrary` — s’il fait des centaines de Mo ou des Go, c’est ça.
3. Au moment du ralenti, CPU de djay dans Moniteur d’activité : s’il grimpe et reste haut, c’est ça.

Sans ton rapport de crash, on reconnaît le bug au **temps** : ça tient, puis ça tombe. Pas à un clic précis.

## Contre

Geste complet : [_kb/outils/FILET-SET.md](../outils/FILET-SET.md).

```bash
bash "_kb/outils/filet-set.sh" avant-set
```

iCloud **OFF** pendant le live. La sync, c’est après. Ne pas vider la bibliothèque : tu perds cues et playlists.
