# Carte musique — partie musicale

Le champ musical entier, pas seulement le losange. Cuisine, herbe : pas ici. Pédagogie : seulement là où un geste musical y a déjà touché.

Règle : [_kb/liens/REGLE.md](REGLE.md).
Perf : [_kb/perf/FONCTION.md](../perf/FONCTION.md).

## Vue d’ensemble

```
                         kb-perf
                      (état, pas musique)
                            ↑
            set DJ · mashup live · voix live · scène
                            │
     voix          losange mashup           mix
                    kb-dj    prod
                      mashup
                    djay  Ableton
                            │
                     outils live / MaxMSP
                            │
                    scène · pedago Ableton
```

Le losange est le cœur déjà nommé. Autour : les autres gestes musicaux. kb-perf reste au-dessus du live, pas au-dessus des dossiers.

## Nœuds

| Nœud | Rôle | Pas ça |
| --- | --- | --- |
| kb-dj | Canon, sets, pratique DJ | Pas l’état de flow |
| djay | Mix DJ, mashup live | Pas Ableton |
| mashup | Geste qui croise live et studio | Pas un outil, pas un hub |
| Prod | Pièces, sessions, extraits | Pas le mix d’écoute |
| Ableton | Session, clips, Push, pièce | Pas djay |
| Voix | Prise, présence, traitement | Pas « la perf » |
| Mix | Bus, balance, extraits de set | Pas la prod |
| Outils live | MaxMSP, looper, code scène | Pas un hub artistique |
| Set DJ | Geste de jouer un set | Pas le losange mashup |

kb-perf n’est **pas** un nœud musical.

---

## 1. Losange mashup (tenu)

Un geste, quatre coins. Le mashup est le croisement.

```
        kb-dj                 prod
           \                 /
            \               /
              mashup
            /               \
           /                 \
        djay               Ableton
```

- **kb-dj** — les sources qui entrent dans le mashup
- **djay** — le mashup joué / trouvé en live
- **Ableton** — le mashup construit / figé en session
- **prod** — le mashup devenu pièce

Les côtés ne s’écrivent pas à part. Ils tiennent parce que le mashup les a déjà tenus.

Un mashup n’est pas un set. Un set peut *contenir* un mashup. Ce n’est pas le même geste.

---

## 2. Set DJ (tenu)

Geste distinct du losange.

```
kb-dj  →  djay  →  set  →  kb-perf
```

- **Geste :** le set se joue dans djay, avec le canon de kb-dj.
- **Statut :** tenu
- **Pas le losange :** Ableton et prod ne sont pas requis. S’il y a mashup dans le set, le losange s’ajoute, il ne remplace pas le set.

---

## 3. Voix (satellite)

La voix est dans la partie musicale. Elle n’est pas un cinquième coin du losange.

### Voix live → kb-perf

- **Geste :** la voix en public est un état, pas seulement une piste.
- **Statut :** tenu pour le live
- Une voix seulement posée en prod **n’écrit pas** ce lien.

Pas encore de lien : Voix → Prod, Voix → djay, Voix → mashup. Aucune session nommée ici.

---

## 4. Mix (tenu)

Le mix écoute et balance. Il n’est pas la prod, ni le set.

### Prod → Mix

- **Geste :** extraits prod et extraits mix publiés ensemble (atelier ARTNOART).
- **Statut :** tenu

### Mix → Set / kb-dj

- **Geste :** *Live Set Excerpt* — le mix pointe déjà vers le set.
- **Statut :** tenu

---

## 5. Outils live / scène (tenu)

### Ableton → Prod

Déjà tenu **dans** le losange quand le geste est un mashup. Hors mashup, Ableton sert aussi les pièces de l’atelier (Push, clips, session). Même outil, autre entrée : on ne recopie pas le côté du losange.

### Outils live → scène

- **Geste :** Bionic Looper (Bionic Orchestra 2.0, Cie Organic Orchestra) déjà joué en spectacle vivant.
- **Statut :** tenu
- MaxMSP / looper restent des outils. Pas un hub.

### Scène → kb-perf

- **Geste :** un outil live joué en public demande un flow.
- **Statut :** tenu pour le spectacle ; un patch seulement ouvert en atelier **n’écrit pas** ce lien.

---

## 6. Sortie hors musique (déjà servie)

### Ableton → pédagogie

- **Geste :** ateliers déjà animés autour d’Ableton Live, Push et MaxMSP.
- **Statut :** tenu
- La pedago n’a pas encore sa carte. Le lien existe : le geste a eu lieu.

---

## kb-perf, depuis la musique

Pas une hiérarchie. Chaque ligne = un geste live qui a besoin de l’état.

| Geste musical | Vers kb-perf | Pas si |
| --- | --- | --- |
| Set DJ | tenu | ranger un fichier djay |
| Mashup live (djay) | tenu | mashup seulement assemblé en prod |
| Voix live | tenu | voix seulement posée en prod |
| Scène / outil live | tenu | patch seulement en atelier |

Une perf culinaire invoquerait le **même** kb-perf. Pas un kb-perf-musique.

---

## Pas de lien (volontairement)

- Voix → Prod, Voix → djay, Voix → mashup
- Découper le losange en ponts djay → Ableton « au cas où »
- Faire du set un losange (il manque prod / Ableton)
- kb-perf au-dessus de kb-dj / Ableton / Prod
- Cuisine, herboristerie (autre carte, jusqu’à un geste réel)

---

## Comment tester

1. Prendre un geste musical réel.
2. Est-ce un mashup des quatre coins ? → losange.
3. Est-ce un set ? → kb-dj → djay → set → kb-perf.
4. Est-ce de la voix, du mix, de la scène ? → leur ligne, pas le losange.
5. Flow ? → kb-perf. Sinon, rien.
6. Hésitation ? → ne rien écrire.
