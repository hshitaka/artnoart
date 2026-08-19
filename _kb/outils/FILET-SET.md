# Filet set — djay

Geste tenu : un set long dans djay, **sans** la sync iCloud sur le dos.

Cause : [_kb/liens/CAUSE-djay.md](../liens/CAUSE-djay.md).
Carte : [_kb/liens/carte-musique.md](../liens/carte-musique.md) § set DJ.

Le script se trouve tout seul. Il copie, il ne supprime rien.

## Avant

1. Ferme djay.
2. Depuis le dépôt artnoart :

```bash
bash "_kb/outils/filet-set.sh" avant-set
```

3. Dans les Réglages iCloud qui s’ouvrent : **djay OFF**.
4. Ouvre djay. Joue.

## Pendant

iCloud djay reste OFF. Pas de sync. Pas de reset. Tu joues.

```bash
bash "_kb/outils/filet-set.sh" pendant
```

## Après

1. Set fini.
2. Puis :

```bash
bash "_kb/outils/filet-set.sh" apres-set
```

3. Dans les Réglages iCloud : **djay ON**.

## Voir

```bash
bash "_kb/outils/filet-set.sh" status
```

La copie est dans `Music/djay-backups/`. L’original reste. L’état du filet aussi (`filet-etat.txt`) — on l’écrit, on ne l’efface pas.
